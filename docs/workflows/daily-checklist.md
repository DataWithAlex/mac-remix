# Daily Prep Checklist

Use this to stay consistent. Time estimate: 20–30 minutes per new batch (as of 28 Sep 2025).

1. **Sync Sources**
   - Download new promos/purchases into `~/Downloads/ToIngest`.
   - Back up yesterday’s `~/Music/DJ` to external SSD (Time Machine handles nightly).

2. **Ingest**
   - Activate virtualenv (`source .venv/bin/activate`).
   - `djprep ingest ~/Downloads/ToIngest` (use `--move` to clean staging).
   - Review `djprep show-manifest` for duplicates.

3. **Analyse / Tag** _(pending automation)_
   - Run Rekordbox/Serato analysis or manual BPM/Key detection.
   - Add `Comment` tags (STEM, Energy, etc.) using Rekordbox tag editor or Mixed In Key.

4. **Stems**
   - Queue high-priority tracks: `djprep stems ~/Music/DJ/Tracks/<file>.mp3`.
   - Rename outputs to `[VOCALS]` etc. if automation not yet applied.

5. **Normalise & Export**
   - Batch-process newly created stems or edits (see `docs/normalization-export.md`).
   - Update MP3 performance copies in `Playlists/Performance`.

6. **Software Sync**
   - Open Serato; Smart Crates update automatically.
   - Open rekordbox; refresh playlists and export to USB if a gig is upcoming.

7. **Controller Check (if available)**
   - Plug DDJ-FLX4, confirm pads toggle stems, verify audio routing.

8. **Log & Archive**
   - Append notable changes to `CHANGELOG.md` (create later) or Git commit messages.
   - Push repo updates (`docs/`, `config/`) to GitHub.

Rinse and repeat; adjust weekly to capture new automation or software changes.
