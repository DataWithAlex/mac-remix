# System Architecture

_Last refreshed: 28 September 2025._

## Goals

- Automate repetitive DJ/remix prep tasks (ingest, rename, stems, tagging, exports).
- Maintain a hybrid organisation model (filesystem + metadata) that any DJ software can consume.
- Keep the core in Python CLI form (scriptable, automation-friendly) while leaving space for future GUI/web layers.
- Integrate smoothly with Serato DJ Lite/Pro and rekordbox 7+ for Pioneer DDJ-FLX4 workflows.

## High-Level Diagram

```
┌───────────┐     ingest      ┌──────────────┐     stems/export     ┌────────────────┐
│ Downloads │ ──────────────▶ │  djprep CLI  │ ───────────────────▶ │ Managed Library │
└───────────┘                 │ (Typer/Rich) │                      │  (Tracks/Stems) │
                               └──────────────┘                      └────────────────┘
                                      │                                         │
                                      │ manifest + metadata                    │ playlists + tags
                                      ▼                                         ▼
                               ┌──────────────┐                        ┌─────────────────┐
                               │ docs/ & ops  │                        │ DJ Software     │
                               │ (playbooks)  │                        │ (Serato, rekord)│
                               └──────────────┘                        └─────────────────┘
```

## Components

| Component | Description | Notes |
|-----------|-------------|-------|
| `src/djprep/cli.py` | Typer-powered CLI with subcommands (`init`, `ingest`, `stems`, `show-manifest`). | Rich tables for feedback, Mutagen integration when available. |
| `config/djprep.yaml` | User-editable YAML controlling library paths, Demucs model, export preferences. | Example config provided; copy before first run. |
| `config/library-manifest.json` | Auto-generated ledger of ingested files (source path, library path, timestamp). | Supports auditing, duplicate detection, playlist seeding. |
| Docs (`docs/`) | Procedures, integration guides, and decision records. | Treated as authoritative runbooks. |

## Key Decisions

### CLI-first, GUI-later

- **Why CLI**: Faster automation, remote/batch-friendly, integrates with launchd or cron. Secondary benefits include easier CI/CD and reproducible logs.
- **GUI plans**: Future Typer+Rich TUI or a Streamlit web dashboard can sit *on top* of the CLI without breaking workflows.

### Hybrid organisation (folders + metadata)

- Filesystem encoding keeps Tracks/Stems/Playlists redundant and portable (crucial for USB exports).
- Metadata (ID3 comment `STEM=...`, BPM, Key) powers Smart Crates (Serato) and Intelligent Playlists (rekordbox).

### Open-source audio tooling

| Task | Preferred Tool | Rationale |
|------|----------------|-----------|
| Stem separation | Demucs (`htdemucs` model) | High-quality offline stems for remixing. |
| BPM detection* | Essentia or librosa | Documented in `docs/stems.md` for future automation. |
| Key detection* | Essentia or KeyFinder CLI | Integration planned post-MVP. |
| Normalisation | `ffmpeg-normalize` (EBU R128) | Consistent loudness for club playback. |

_*Implementation scheduled for v0.2; meanwhile DJ software analysis remains valid._

### DJ software integration strategy

1. **Serato**: Leverage Smart Crates and built-in Stems pad mode for the DDJ-FLX4. Use Serato Tools (future) for crate automation.
2. **rekordbox**: Use XML imports or folder sync, Intelligent Playlists, and Track Separation mapped via MIDI learn.
3. **DAWs**: Provide well-labelled stems plus optional Ableton/Logic templates (see `docs/integration/daws.md`).

### Safety & Backups

- Git tracks documentation and CLI configuration, not audio assets (audio folders excluded via `.gitignore`).
- `config/library-manifest.json` acts as a secondary ledger for quick restore/resync.
- Encourage `Time Machine` or cloud backup for `~/Music/DJ` (documented in `docs/workflows/daily-checklist.md`).

## Roadmap Snapshot (as of 0.1.0)

| Version | Focus |
|---------|-------|
| 0.1.0 | Folder skeleton, ingestion CLI, docs, Demucs wrapper. |
| 0.2.0 | BPM/key analysis, comment tagging, ffmpeg-normalise integration, Rekordbox XML export. |
| 0.3.0 | Serato crate writer, Ableton Live Set templating, Streamlit dashboard (optional). |

Feature tickets should capture upstream version dependencies (e.g. Demucs 4.0, rekordbox 7.0.2) and revalidate instructions each quarter.
