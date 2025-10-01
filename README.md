# mac-remix: Python-Based DJ & Remix Library Management

mac-remix is a Python toolkit and documentation set that turns your macOS workstation into a DJ/remix preparation hub. It combines a reproducible folder structure, Typer-based CLI, and step-by-step guides for integrating with Serato DJ Lite/Pro, rekordbox 7+, and the Pioneer DDJ-FLX4 controller. The goal is to automate repetitive prep work—ingesting tracks, creating stems, tagging BPM/keys, normalising audio—and hand off a performance-ready library to your DJ software.

> **Current date:** 01 October 2025. All references to "today" in the docs resolve to this date so future you can spot when instructions need refreshing.

---

## Repository Layout

```
mac-remix/
├── README.md
├── AGENTS.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── config/
│   └── djprep.example.yaml
├── src/
│   └── djprep/
│       ├── __init__.py
│       └── cli.py
└── docs/
    ├── README.md
    ├── architecture.md
    ├── preflight-mac.md
    ├── folder-structure.md
    ├── ingestion.md
    ├── stems.md
    ├── normalization-export.md
    ├── integration/
    │   ├── serato.md
    │   ├── rekordbox.md
    │   └── daws.md
    └── workflows/
        ├── daily-checklist.md
        └── usb-export.md
```

---

## Quick Start (first push checklist)

1. **Git init** (already handled by this repo scaffold, see below for verification).
2. **Create a Python virtual environment** and upgrade `pip`:
   ```bash
   cd /Users/alexsciuto/Library/Mobile\ Documents/com~apple~CloudDocs/DataWithAlex/mac-remix
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   ```
3. **Run the guided setup helper** (installs the package, copies config, runs `djprep init`):
   ```bash
   python scripts/setup_repo.py
   ```
   Accept the default library root (`./library`) or point it at another path when prompted.
4. **Ingest your first `.mp3` track** (see [Ingesting MP3s](#ingesting-mp3s-step-by-step)).
5. **Read the integration docs** under `docs/integration/` to connect your DJ software before plugging in the DDJ-FLX4.

After you are satisfied, stage files with `git add .` and push to GitHub (`git commit -m "Initial commit" && git remote add origin <URL> && git push -u origin main`).

---

## Ingesting MP3s (step-by-step)

1. **Drop new music into a staging folder** (e.g., `~/Downloads/new-tracks`).
2. **Run the ingest command** to copy them into your managed library, optionally overriding artist/title:
   ```bash
   djprep ingest ~/Downloads/new-tracks/*.mp3
   # or with manual metadata
   djprep ingest "~/Downloads/Track.mp3" --artist "Artist" --title "Track (Extended Mix)"
   ```
3. **What happens automatically**:
   - Files are copied to `library/Tracks/Artist - Title.mp3` (or the folder you configured).
   - Each ingest is logged inside `config/library-manifest.json` so you can audit changes.
   - The CLI reminds you of next steps: run stems, analysis, or exports.
4. **Verify inside your DJ application**:
   - Drag `library/Tracks/` (or your configured location) into Serato or use rekordbox `File ▸ Import Folder…`.
   - Smart Crates/Intelligent Playlists populate based on the metadata written in later steps.
5. **Continue with stems or normalization** using the workflows in `docs/workflows/`.

⚠️ Tip: Use the `--move` flag if you want files removed from the staging folder after ingestion.

---

## CLI Overview

| Command          | Purpose                                                                                          |
|------------------|--------------------------------------------------------------------------------------------------|
| `djprep init`    | Creates/validates library folders defined in `config/djprep.yaml`.                               |
| `djprep ingest`  | Copies or moves `.mp3/.wav/.flac/.m4a` into library using clean naming, updates manifest.        |
| `djprep stems`   | Runs [Demucs](https://github.com/facebookresearch/demucs) with your configured model to create stems. |
| `djprep show-manifest` | Prints a table (Rich) of every ingested track and its file path.                            |

Future releases (documented in `docs/architecture.md`) include BPM/key analysis, loudness normalisation, Rekordbox XML export, and Serato crate generation.

---

## Software Integration Summary

| Software      | Usage in this repo                                                                                                 | Key docs |
|---------------|---------------------------------------------------------------------------------------------------------------------|----------|
| Serato DJ Lite/Pro (3.2+) | Plug-and-play with DDJ-FLX4. Smart Crates watch `Comment` strings like `STEM=VOCALS`. Stems pad mode is enabled in `Setup ▸ DJ Preferences`. | `docs/integration/serato.md` |
| rekordbox 7+  | Import the managed folders, map Track Separation to a pad layer, and use Intelligent Playlists for automatic sorting. | `docs/integration/rekordbox.md` |
| Ableton Live 12 / Logic Pro 11 | Consume the offline stems for remix production; optional AppleScript automation is described for quick project templating. | `docs/integration/daws.md` |

The `docs/` tree also covers optional beets integration, ffmpeg-normalise usage, and USB export routines for club gear.

---

## Hardware: Pioneer DDJ-FLX4

- **Connection**: USB-C straight into the Mac. Driverless on macOS 14.6+. Set as the audio interface inside Serato/rekordbox (documented on 28 Sep 2025).
- **Serato workflow**: Replace Sampler/Pad mode with Stems, use Smart Fader & Smart CFX for quick transitions, and load offline stems as additional tracks for mashups.
- **rekordbox workflow**: Enable Track Separation via `Preferences ▸ Extensions ▸ Track Separation`, then MIDI-learn the Vocal/Bass/Drums toggles to the FLX4 pads.
- **Pre-arrival prep**: Even without the controller, you can install Serato/rekordbox, build libraries, and use macOS’ virtual audio device to audition stems—see `docs/preflight-mac.md`.

---

## Documentation Highlights

- `docs/architecture.md`: System components, data flow, and decisions (CLI vs GUI, tagging model, integration boundaries).
- `docs/folder-structure.md`: How Tracks/Stems/Playlists map to DJ use cases, naming conventions, and backup strategy.
- `docs/workflows/ingestion.md`: Deep dive on ingesting music, reading/writing ID3 tags, deduplication, and manifest usage.
- `docs/stems.md`: Offline stem extraction using Demucs, naming, manifests, and how to surface stems inside Serato/rekordbox.
- `docs/normalization-export.md`: ffmpeg-normalise recipes, LUFS targets, and best practices for MP3 performance copies.
- `docs/integration/*.md`: Software and hardware specifics, screenshots callouts, and config values.
- `docs/workflows/usb-export.md`: Club-ready USB export pipeline (rekordbox XML, Serato USB helper, checksum verification).

---

## Next Steps & Contributions

- The `AGENTS.md` file documents coding-agent conventions so future automation stays consistent.
- Run `ruff`/`black` (defined as optional developer dependencies) before pushing if you add code.
- Use GitHub Projects or Issues to track enhancements (BPM/key analysis, Rekordbox XML writer, Serato crate generator).

Happy prepping and see you on the dancefloor!
