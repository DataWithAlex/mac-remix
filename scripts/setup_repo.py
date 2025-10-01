#!/usr/bin/env python3
"""Interactive bootstrapper for the mac-remix repository."""
from __future__ import annotations

import shlex
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = REPO_ROOT / "config"
EXAMPLE_CONFIG = CONFIG_DIR / "djprep.example.yaml"
ACTIVE_CONFIG = CONFIG_DIR / "djprep.yaml"
RAW_SONG_DIR = REPO_ROOT / "raw-songs"
DEFAULT_LIBRARY_ROOT = "./library"


def banner() -> None:
    print("=" * 72)
    print("mac-remix setup helper")
    print("This script prepares your virtualenv, config, and library folders.")
    print("Repo root:", REPO_ROOT)
    print("Python:", sys.executable)
    print("=" * 72)


def require_repo_root() -> None:
    if not (REPO_ROOT / "pyproject.toml").exists():
        print("✖ pyproject.toml not found. Run this script from the repo root.")
        sys.exit(1)


def ensure_virtualenv() -> None:
    if sys.prefix == sys.base_prefix:
        print("✖ No virtual environment detected.")
        reply = input("Create .venv now? [Y/n] ").strip().lower() or "y"
        if reply.startswith("y"):
            print("→ Creating .venv via python3 -m venv .venv")
            subprocess.run(
                [sys.executable, "-m", "venv", ".venv"], cwd=REPO_ROOT, check=True
            )
            print("✔ Created .venv. Activate it with: source .venv/bin/activate")
        else:
            print("ℹ Activate your virtual environment and rerun this script.")
        sys.exit(0)


def prompt_library_root() -> str:
    current = DEFAULT_LIBRARY_ROOT
    if ACTIVE_CONFIG.exists():
        for line in ACTIVE_CONFIG.read_text().splitlines():
            if line.strip().startswith("library_root:"):
                current = line.split(":", 1)[1].strip().strip("\"'")
                break
    prompt = f"Library root path [{current}]: "
    reply = input(prompt).strip()
    return reply or current


def copy_config() -> None:
    if not EXAMPLE_CONFIG.exists():
        print(f"✖ Missing example config at {EXAMPLE_CONFIG}")
        sys.exit(1)
    if ACTIVE_CONFIG.exists():
        print(f"✔ Found existing config: {ACTIVE_CONFIG}")
        return
    shutil.copy(EXAMPLE_CONFIG, ACTIVE_CONFIG)
    print(f"✔ Copied example config to {ACTIVE_CONFIG}")


def update_config_library_root(new_root: str) -> None:
    lines = ACTIVE_CONFIG.read_text().splitlines()
    updated = False
    for idx, line in enumerate(lines):
        if line.strip().startswith("library_root:"):
            indent = line[: len(line) - len(line.lstrip())]
            lines[idx] = f'{indent}library_root: "{new_root}"'
            updated = True
            break
    if not updated:
        lines.insert(0, f'library_root: "{new_root}"')
    ACTIVE_CONFIG.write_text("\n".join(lines) + "\n")
    print(f"✔ Set library_root to {new_root}")


def ensure_raw_folder() -> None:
    if RAW_SONG_DIR.exists():
        print(f"✔ raw-songs directory already present: {RAW_SONG_DIR}")
        return
    RAW_SONG_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✔ Created raw song drop folder: {RAW_SONG_DIR}")


def run_command(cmd: list[str], description: str, check: bool = True) -> bool:
    print(f"\n→ {description}")
    print("   $", " ".join(shlex.quote(part) for part in cmd))
    proc = subprocess.run(cmd, cwd=REPO_ROOT, text=True)
    success = proc.returncode == 0
    if success:
        print("   ✔ done")
    else:
        print(f"   ✖ exit code {proc.returncode}")
        if check:
            sys.exit(proc.returncode)
    return success


def install_package() -> None:
    regular_cmd = [sys.executable, "-m", "pip", "install", "."]
    if run_command(regular_cmd, "Installing djprep") and verify_import():
        return

    print("! Standard install did not load djprep; attempting editable fallback.")
    editable_cmd = [sys.executable, "-m", "pip", "install", "-e", "."]
    run_command(editable_cmd, "Installing djprep in editable mode")
    if not verify_import():
        print("✖ Unable to import djprep after installation. Check pip output above.")
        sys.exit(1)


def verify_import() -> bool:
    code = "import importlib; importlib.import_module('djprep')"
    result = subprocess.run([sys.executable, "-c", code], cwd=REPO_ROOT)
    if result.returncode == 0:
        print("   ✔ djprep import verified")
        return True
    print("   ✖ djprep import failed")
    return False


def initialize_library() -> None:
    run_command(
        [sys.executable, "-m", "djprep.cli", "init"],
        "Bootstrapping library folders with djprep init",
    )


def finalize(new_root: str) -> None:
    print("\nSetup complete! Next steps:")
    print(
        f"  • Drop new tracks into {RAW_SONG_DIR} and ingest with: djprep ingest raw-songs/Your_Track.mp3"
    )
    print(
        f"  • Import {REPO_ROOT / new_root} into Rekordbox (see docs/integration/rekordbox.md)"
    )
    print("  • Re-run this script anytime to reconfigure or reinstall.")


def main() -> None:
    banner()
    require_repo_root()
    ensure_virtualenv()
    copy_config()
    library_root = prompt_library_root()
    update_config_library_root(library_root)
    ensure_raw_folder()
    install_package()
    initialize_library()
    finalize(library_root)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted by user.")
        sys.exit(1)
