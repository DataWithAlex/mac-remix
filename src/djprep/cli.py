from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional

import typer
import yaml
from rich.console import Console
from rich.table import Table

try:
    from mutagen import File as MutagenFile
except ImportError:  # pragma: no cover - optional at runtime
    MutagenFile = None  # type: ignore

app = typer.Typer(help="Command-line utilities for the djprep workflow.")
console = Console()

DEFAULT_CONFIG = Path("config/djprep.yaml")
FALLBACK_CONFIG = Path("config/djprep.example.yaml")
MANIFEST_PATH = Path("config/library-manifest.json")
SUPPORTED_AUDIO = {".mp3", ".wav", ".flac", ".m4a", ".aiff", ".aif"}


class ConfigError(Exception):
    """Raised when configuration values are missing or invalid."""


def load_config(config_path: Path | None = None) -> dict:
    """Load YAML config, falling back to the example file."""
    path = config_path or DEFAULT_CONFIG
    if path.exists():
        cfg_path = path
    elif FALLBACK_CONFIG.exists():
        cfg_path = FALLBACK_CONFIG
        console.print(
            f"[yellow]Config not found at {path}; using example config {cfg_path}.\n"
            "Copy it to config/djprep.yaml and adjust values when ready.[/yellow]"
        )
    else:
        raise ConfigError(
            f"No configuration file found at {path} or fallback {FALLBACK_CONFIG}."
        )

    with cfg_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    return data


def expand_path(raw: str) -> Path:
    return Path(raw).expanduser().resolve()


def library_paths(config: dict) -> dict:
    root = expand_path(config.get("library_root", "~/Music/DJ"))
    tracks = root / config.get("tracks_subdir", "Tracks")
    stems = root / config.get("stems_subdir", "Stems")
    playlists = root / config.get("playlists_subdir", "Playlists")
    return {"root": root, "tracks": tracks, "stems": stems, "playlists": playlists}


def ensure_library(config: dict) -> None:
    paths = library_paths(config)
    created: list[str] = []
    for key, directory in paths.items():
        if key == "root":
            directory.mkdir(parents=True, exist_ok=True)
        else:
            if not directory.exists():
                directory.mkdir(parents=True, exist_ok=True)
                created.append(str(directory))
    if created:
        console.print("[green]Created library directories:[/green]")
        for path in created:
            console.print(f"  • {path}")


def _gather_audio(inputs: Iterable[Path]) -> List[Path]:
    audio_files: List[Path] = []
    for item in inputs:
        if item.is_dir():
            for candidate in item.rglob("*"):
                if candidate.is_file() and candidate.suffix.lower() in SUPPORTED_AUDIO:
                    audio_files.append(candidate)
        elif item.is_file() and item.suffix.lower() in SUPPORTED_AUDIO:
            audio_files.append(item)
        else:
            console.print(f"[yellow]Skipping unsupported path: {item}[/yellow]")
    return sorted(audio_files)


def _infer_tags(path: Path) -> tuple[Optional[str], Optional[str]]:
    if MutagenFile is None:
        return None, None
    try:
        metadata = MutagenFile(path)
    except Exception:  # pragma: no cover - best effort only
        return None, None
    if not metadata:
        return None, None
    artist = None
    title = None
    for key in ("artist", "ARTIST"):
        value = metadata.tags.get(key) if metadata.tags else None
        if value:
            if isinstance(value, list):
                artist = str(value[0])
            else:
                artist = str(value)
            break
    for key in ("title", "TITLE"):
        value = metadata.tags.get(key) if metadata.tags else None
        if value:
            if isinstance(value, list):
                title = str(value[0])
            else:
                title = str(value)
            break
    return artist, title


def _sanitize(text: str) -> str:
    safe = [c for c in text if c not in {"/", "\\", ":", "*", "?", "\"", "<", ">", "|"}]
    collapsed = " ".join(str("".join(safe)).split())
    return collapsed.strip()


def _target_filename(source: Path, artist: Optional[str], title: Optional[str]) -> str:
    base = source.stem
    if artist and title:
        base = f"{_sanitize(artist)} - {_sanitize(title)}"
    elif artist:
        base = f"{_sanitize(artist)} - {_sanitize(source.stem)}"
    elif title:
        base = _sanitize(title)
    else:
        base = _sanitize(base)
    return f"{base}{source.suffix.lower()}"


def _update_manifest(entry: dict) -> None:
    manifest = {"tracks": []}
    if MANIFEST_PATH.exists():
        try:
            manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            console.print(
                f"[yellow]Manifest at {MANIFEST_PATH} unreadable; starting fresh.[/yellow]"
            )
    manifest.setdefault("tracks", [])
    manifest["tracks"].append(entry)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")


@app.command()
def init(config_path: Optional[Path] = typer.Option(None, "--config", "-c", help="Path to djprep configuration YAML")) -> None:
    """Create the folder skeleton under the configured library root."""
    config = load_config(config_path)
    ensure_library(config)
    paths = library_paths(config)
    table = Table(title="Library Paths", box=None)
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Path", style="white")
    for key, value in paths.items():
        table.add_row(key, str(value))
    console.print(table)


@app.command()
def ingest(
    inputs: List[Path] = typer.Argument(..., help="Audio files or directories to ingest."),
    artist: Optional[str] = typer.Option(None, help="Override artist tag for all files."),
    title: Optional[str] = typer.Option(None, help="Override title tag (useful for single track ingest)."),
    move: bool = typer.Option(False, "--move", help="Move files instead of copying."),
    config_path: Optional[Path] = typer.Option(None, "--config", "-c", help="Path to configuration file."),
) -> None:
    """Place audio files into the Tracks folder with clean naming and log manifest entries."""
    config = load_config(config_path)
    ensure_library(config)
    paths = library_paths(config)
    tracks_dir: Path = paths["tracks"]
    files = _gather_audio(p.expanduser() for p in inputs)
    if not files:
        console.print("[red]No supported audio files found to ingest.[/red]")
        raise typer.Exit(1)

    console.print(f"[green]Preparing to ingest {len(files)} file(s) into {tracks_dir}[/green]")

    for source in files:
        inferred_artist, inferred_title = _infer_tags(source)
        file_artist = artist or inferred_artist
        file_title = title or inferred_title
        target_name = _target_filename(source, file_artist, file_title)
        destination = tracks_dir / target_name
        destination.parent.mkdir(parents=True, exist_ok=True)
        operation = shutil.move if move else shutil.copy2
        operation(source, destination)
        console.print(f"  • {'Moved' if move else 'Copied'} {source} → {destination}")
        _update_manifest(
            {
                "source": str(source.resolve()),
                "library_path": str(destination),
                "artist": file_artist,
                "title": file_title,
                "ingested_at": datetime.now().isoformat(timespec="seconds"),
            }
        )

    console.print(
        "[green]Ingestion complete.[/green] Review docs/workflows/ingestion.md for next steps "
        "(stems, analysis, exports)."
    )


@app.command()
def stems(
    inputs: List[Path] = typer.Argument(..., help="Audio files to separate using Demucs."),
    config_path: Optional[Path] = typer.Option(None, "--config", "-c", help="Config path"),
    model: Optional[str] = typer.Option(None, help="Demucs model name (overrides config)."),
    dry_run: bool = typer.Option(False, help="Show commands without executing."),
) -> None:
    """Run Demucs stem separation and stage results inside the Stems folder."""
    config = load_config(config_path)
    paths = library_paths(config)
    stems_root: Path = paths["stems"]
    ensure_library(config)
    files = _gather_audio(p.expanduser() for p in inputs)
    if not files:
        console.print("[red]No supported audio files found for stem extraction.[/red]")
        raise typer.Exit(1)

    model_name = model or config.get("stem_model", "htdemucs")
    demucs_cmd = shutil.which("demucs")
    if demucs_cmd is None:
        console.print(
            "[red]Demucs executable not found. Install demucs via pip and ensure it is on your PATH.[/red]"
        )
        raise typer.Exit(1)

    for file_path in files:
        output_dir = stems_root
        cmd = [
            demucs_cmd,
            "-n",
            model_name,
            "-o",
            str(output_dir),
            str(file_path),
        ]
        console.print(f"[cyan]Running: {' '.join(cmd)}[/cyan]")
        if dry_run:
            continue
        subprocess.run(cmd, check=True)
    console.print(
        "[green]Demucs processing complete. Use docs/stems.md to move/rename outputs.[/green]"
    )


@app.command()
def show_manifest() -> None:
    """Display the ingested track manifest for quick reference."""
    if not MANIFEST_PATH.exists():
        console.print("[yellow]Manifest file not found. Ingest tracks first.[/yellow]")
        raise typer.Exit(1)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    table = Table(title="Library Manifest", show_lines=False)
    table.add_column("Artist", style="magenta")
    table.add_column("Title", style="cyan")
    table.add_column("Library Path", style="white")
    table.add_column("Ingested", style="green")
    for entry in manifest.get("tracks", []):
        table.add_row(
            entry.get("artist") or "—",
            entry.get("title") or Path(entry.get("library_path", "")).stem,
            entry.get("library_path", ""),
            entry.get("ingested_at", ""),
        )
    console.print(table)


def main() -> None:  # pragma: no cover - Typer entry point
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
