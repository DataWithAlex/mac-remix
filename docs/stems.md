# Stem Extraction & Management

_Last validated: 28 Sep 2025 (Demucs 4.0)._ 

## Overview

Offline stems deliver higher fidelity than real-time separation. The workflow here produces four stems (`VOCALS`, `DRUMS`, `BASS`, `OTHER`) per track, ready for DJ software or DAW remixing.

## Requirements

- Python package `demucs>=4.0.0` (installed via `pip install demucs`).
- FFmpeg (Homebrew: `brew install ffmpeg`).
- Configured library (`djprep init`).

## Command

```bash
# Dry run (shows demucs command without executing)
djprep stems ~/Music/DJ/Tracks/Artist\ -\ Title.mp3 --dry-run

# Execute with default model (htdemucs)
djprep stems ~/Music/DJ/Tracks/Artist\ -\ Title.mp3

# Custom model
djprep stems track.mp3 --model mdx_extra
```

### Output

Demucs writes to `<Stems Root>/<model>/<Artist - Title>/`. After the run, tidy up:

```bash
# Example relocation (planned automation in v0.2)
mkdir -p "~/Music/DJ/Stems/Artist - Title"
mv "~/Music/DJ/Stems/htdemucs/Artist - Title/vocals.wav" "~/Music/DJ/Stems/Artist - Title/Artist - Title [VOCALS].wav"
# Repeat for drums/bass/other.
```

Planned: automatic rename/move post-processing step inside CLI.

## Post-Processing

1. **Normalise (optional)**: See `docs/normalization-export.md` for LUFS targets.
2. **Tag Comments**: Use Mutagen or future CLI command to write `COMMENT=STEM=VOCALS` etc. Serato/rekordbox rules depend on this.
3. **Manifest**: Add manual note to `config/library-manifest.json` or create individual `manifest.json` inside each stems folder (example template in `config/djprep.example.yaml`).

## Serato Integration

- **Smart Crates**: Create crates with rule `Comment → contains → STEM=VOCALS` etc.
- **Pad Mapping**: Serato DJ Lite/Pro 3.2+ allows replacing Sampler with Stems. FLX4 pads toggle Vocal/Melody/Bass/Drums (documented in `docs/integration/serato.md`).
- **Usage**: Load `Artist - Title.mp3` on Deck 1, `Artist - Title [VOCALS].wav` on Deck 2 for mashups, or rely on Serato’s real-time stems when you only need toggles.

## rekordbox Integration

- **Track Separation**: Enable in Preferences ▸ Extensions ▸ Track Separation, map the FLX4 pads via MIDI Learn.
- **Sampler Method**: Drop offline stems into the rekordbox Sampler slots for finger-drumming while the full mix plays.
- **Intelligent Playlists**: Rule `Comments contains STEM=` ensures stems stay discoverable.

## DAW Usage

- See `docs/integration/daws.md` for importing stems into Ableton Live or Logic Pro with song templates.

## Quality Notes

- `htdemucs` is balanced for DJ use (fast + quality). For acapella-heavy sets, test `mdx_extra_q` (slower, cleaner vocals).
- Keep the original mix alongside stems. Live DJ software (Serato/rekordbox) may still need the full track for waveform/beatgrid.
- Demucs outputs 44.1 kHz WAV by default; convert to FLAC/MP3 if storage is tight (post-normalisation).

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `Demucs executable not found` | Ensure `pip install demucs` ran inside your active virtualenv; re-open terminal. |
| Slow processing | Use GPU (`pip install torch` + CUDA-compatible hardware) or queue overnight. |
| Artefacts in stems | Try alternate models (`mdx_q`, `hdemucs_mmi`). |
| Files overwritten | Keep stems per-track folder; do not run demucs into the root without subdirectories. |

Keep actual audio outside Git; only commit manifests/config/scripts.
