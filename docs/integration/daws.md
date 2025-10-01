# DAW Integration (Ableton Live, Logic Pro)

Updated: 28 Sep 2025.

## Ableton Live 12

### Template Project

1. Create a new Live Set with four audio tracks labelled `VOCALS`, `DRUMS`, `BASS`, `OTHER`.
2. Drop a Limiter and EQ on each channel for quick mixing.
3. Save as `~/Music/Ableton/User Library/Templates/DJ Stem Template.als`.
4. Duplicate the template into `docs/assets/ableton/` (optional) for sharing.

### Import Workflow

1. In Finder, drag the stems folder (`~/Music/DJ/Stems/Artist - Title/`) into the Live browser.
2. Select all four stems, drag onto the template tracks.
3. Warp settings: disable Warp for percussive stems if you prefer manual timing; enable Complex Pro for vocals.
4. Set project tempo to the track BPM (from manifest or Rekordbox analysis).

### Exporting

- Render edited mixdowns to `~/Music/DJ/Tracks/Artist - Title (Edit).wav`.
- Re-ingest with `djprep ingest` to keep library consistent.

## Logic Pro 11

### Project Template

1. File ▸ New from Template ▸ `DJ Stem Template` (create one once with four tracks + bus FX).
2. Import stems via `File ▸ Import ▸ Audio…`.
3. Use Smart Tempo to align if the track drifts; set the project key to the detected key.

### Bounce Settings

- PCM, WAV, 24-bit, 44.1 kHz for mastering.
- MP3 320 kbps for quick performance versions (Logic writes ID3 tags automatically—verify before ingesting).

## Metadata Round-Trip

1. After rendering a new edit, open Rekordbox/Serato to reanalyse or update BPM/Key.
2. Use `Mutagen` (Python) or MetaBliss (GUI) to set `Comment` = `STEM=...` if you create additional stems (e.g., `PIANO`).
3. Update `config/library-manifest.json` manually or via future automation script to track edits.

## Optional Automation

- **Ableton Python Scripts**: Investigate `pyableton` to auto-populate clips from stems.
- **Logic AppleScript**: Use `osascript` to open Logic and load stems automatically (documented in roadmap).

## Storage Tips

- Keep raw multitrack project files outside `~/Music/DJ` (e.g., `~/Music/Projects`), but render final outputs into the managed library so DJ software sees them.
- Version project files using Git LFS or cloud storage to avoid bloating this repo.
