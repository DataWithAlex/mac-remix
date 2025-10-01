# macOS Preflight Checklist (before the DDJ-FLX4 arrives)

_Updated: 01 October 2025 (macOS Sonoma 14.6)._

## 1. System Requirements

- macOS 12.6 or newer (Sonoma 14.x recommended for FLX4 driverless support).
- At least 30 GB free disk (stems consume space; Demucs outputs ~500 MB per track at 44.1 kHz WAV).
- Homebrew installed (`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`).

## 2. Install Core Tools

```bash
# Audio tooling
brew install ffmpeg
```

(Optional) add formatting helpers once the virtualenv is online:
`pip install ruff black`.

## 3. Bootstrap The Repo

```bash
cd /Users/alexsciuto/Library/Mobile\ Documents/com~apple~CloudDocs/DataWithAlex/mac-remix
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python scripts/setup_repo.py
```

The helper script will:
- copy `config/djprep.example.yaml` ➜ `config/djprep.yaml` and ask for the library root (defaults to `./library`).
- install `djprep` (tries editable mode first, then falls back to regular install if needed).
- create `raw-songs/` and run `djprep init` so `library/Tracks`, `library/Stems`, and `library/Playlists` exist.

If you prefer to manage things manually, follow the prompts as a guide and run the equivalent commands yourself.

Confirm the following repo-relative folders exist afterwards:
- `library/Tracks`
- `library/Stems`
- `library/Playlists`

## 4. Install DJ Software

| Software | Download (28 Sep 2025) | Notes |
|----------|-----------------------|-------|
| Serato DJ Lite 3.2+ | https://serato.com/dj/lite/downloads | Unlocks with DDJ-FLX4; Lite is sufficient for stems mode. |
| Serato DJ Pro (optional) | https://serato.com/dj/pro/downloads | Required for recording sets / advanced FX. |
| rekordbox 7.0.2+ | https://rekordbox.com/en/download/ | Free Core plan supports FLX4 control mode. |

Install both and sign into Pioneer DJ account (rekordbox) ahead of time.

## 5. Prepare Virtual Audio (Optional but handy)

If you want to audition stems before the controller arrives:
- Install BlackHole (https://existential.audio/blackhole/) or use macOS’ **Aggregate Device** to route audio back into your headphones.
- In Serato/rekordbox, set audio device to BlackHole and use your Mac keyboard for transport.

## 6. Controller Readiness

- Bookmark Pioneer DDJ-FLX4 support page (https://www.pioneerdj.com/en/support/documents/ddj-flx4/).
- Download the user manual PDF and keep it in your iCloud Drive for offline reference.
- Order a USB-C ↔ USB-A cable if your Mac only has USB-A (FLX4 ships with USB-C ↔ USB-C).

## 7. Test Workflow Without Hardware

1. Ingest a demo MP3 via `djprep ingest`.
2. Launch Serato, import `~/Music/DJ/Tracks`, and check Smart Crate rules (see `docs/integration/serato.md`).
3. Launch rekordbox, import the same folder, and build Intelligent Playlists.
4. Run `djprep stems <track>` (dry run first) to ensure Demucs is callable.
5. Open `config/library-manifest.json` to confirm entries are created.

## 8. Backup Strategy

- Enable Time Machine for `~/Music/DJ` (System Settings ▸ General ▸ Time Machine).
- Optional: sync the `~/Music/DJ` folder to iCloud Drive or external SSD.
- Store `config/djprep.yaml` in Git (this repo) so your config travels with you.

By completing this checklist before the DDJ-FLX4 is in hand, you can plug in and perform immediately upon arrival.
