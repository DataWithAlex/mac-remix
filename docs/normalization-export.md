# Normalisation & Export

As of 28 Sep 2025, Pioneer CDJ/rekordbox players do not auto-normalise track loudness. Normalising once during export keeps your sets consistent.

## Target Values

- **Integrated loudness**: -8.5 LUFS (aggressive club mix) or -10 LUFS (open-format sets).
- **True peak**: -1.0 dBTP to avoid inter-sample clipping on export hardware.
- **Sample rate**: 44.1 kHz (standard for DJ playback), unless your source is 48 kHz—then keep 48 kHz for video sets.

## Tools

- `ffmpeg-normalize` (Python package) wraps FFmpeg’s `loudnorm` filter.
- Raw FFmpeg commands for custom pipelines.
- `pydub` for quick peak normalisation (less recommended for final masters).

## Example: Normalise & Export to MP3 320 kbps

```bash
# Assume you ran djprep stems/ingest already
source .venv/bin/activate

ffmpeg-normalize "~/Music/DJ/Tracks/Artist - Title.wav" \
  -o "~/Music/DJ/Tracks/Artist - Title (Normalized).wav" \
  -tn -8.5 -tp -1.0 -f

ffmpeg -y -i "~/Music/DJ/Tracks/Artist - Title (Normalized).wav" \
  -ar 44100 -b:a 320k "~/Music/DJ/Tracks/Artist - Title.mp3"
```

### Batch Export Script (pseudo)

Planned CLI extension (`djprep export`) will:
1. Iterate over tracks in `Tracks/`.
2. Normalise to target LUFS.
3. Convert to MP3 320 kbps (or another configured codec).
4. Drop results inside `Playlists/Performance/` for quick Serato/rekordbox imports.

## Rekordbox USB Export Tips

1. After normalisation, re-import/refresh in rekordbox.
2. Rekordbox can write analysed track gain to USB. If files are already normalised, disable playback auto-gain to prevent double attenuation.
3. Use `docs/workflows/usb-export.md` for checksum verification before heading to the club.

## Serato Considerations

- Serato applies Auto Gain. Even with pre-normalised files, keep Auto Gain enabled to compensate for any residual differences.
- When exporting crates for another computer, include the normalised files and the `Serato` folder containing crate metadata.

## DAW Finishing

- For remix deliverables, keep 24-bit WAV masters separate from your DJ library to avoid lossy recompression.
- Use loudness meter plugins (Youlean, FabFilter Pro-L2) to cross-check the FFmpeg measurements if you master tracks in a DAW.

## Troubleshooting

| Symptom | Remedy |
|---------|--------|
| `ffmpeg-normalize` missing | Run `pip install ffmpeg-normalize`; ensure FFmpeg is in PATH (`brew install ffmpeg`). |
| MP3 sounds distorted | Lower target loudness (e.g., -10 LUFS) or ensure true peak limit is <= -1.0. |
| ReplayGain tags removed | Reapply using `ffmpeg-normalize --keep-loudness` or run ReplayGain scanner afterwards. |

Keep original WAV/FLAC masters for archival; MP3 exports live in the performance folder for quick reloads.
