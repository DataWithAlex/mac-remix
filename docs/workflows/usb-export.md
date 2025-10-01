# USB Export Workflow (Club Ready)

Last validated: 28 Sep 2025.

## 1. Prepare Playlists

- Ensure rekordbox playlists are up to date (Intelligent Playlists capture new tracks automatically).
- For Serato, create a mirror crate dedicated to the gig (drag in tracks/stems).

## 2. Format USB Drive

- Use Disk Utility → Erase → ExFAT (for 64 GB+) or FAT32 (for CDJ compatibility up to 32 GB).
- Label drive with date + gig (e.g., `2025-09-29-Club`).

## 3. rekordbox Export (for CDJs)

1. Right-click the target playlist → `Export to <USB>`.
2. Enable `Convert beatgrid information` and `Include memory cues`.
3. After export, rekordbox writes analysis, waveforms, and metadata to the USB.

## 4. Serato USB Helper (optional)

If playing on another Serato laptop:

1. Install `serato-tools` (`pip install serato-tools`).
2. Run `serato_tools usb --source ~/Music/_Serato_ --destination /Volumes/2025-09-29-Club`.
3. Copy corresponding audio files (`~/Music/DJ/Tracks`, `~/Music/DJ/Stems`) onto the drive.

## 5. Verify Audio Integrity

```bash
# Example checksum script (run inside repo root)
find /Volumes/2025-09-29-Club -type f -name '*.mp3' -o -name '*.wav' \
  -print0 | xargs -0 shasum -a 256 > ./config/usb-2025-09-29.sha256

# Later verify
shasum -a 256 -c ./config/usb-2025-09-29.sha256
```

Keep the checksum file in Git for audit (do **not** commit the audio).

## 6. Safety Checks

- Eject USB safely; test on another machine or player if possible.
- Bring a backup drive.
- Carry your laptop with Serato/rekordbox + FLX4 as fallback.

## 7. Post-Gig

- Update `library-manifest.json` with any live edits you made (rename, hot cues).
- Copy history from rekordbox/Serato back into this repo’s `docs/` for set logs.

Regularly rotate USB drives to prevent wear; keep one labelled emergency backup in your gig bag.
