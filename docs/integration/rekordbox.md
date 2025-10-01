# rekordbox Integration (DDJ-FLX4)

_Status as of 28 Sep 2025: rekordbox 7.0.2._

## 1. Import Library

1. Launch rekordbox and sign in to your Pioneer DJ account.
2. Go to `File ▸ Import ▸ Folder…` and select `~/Music/DJ/Tracks`.
3. Repeat for `~/Music/DJ/Stems` if you want stems available as separate tracks or sampler sources.
4. rekordbox stores references; re-importing a folder updates metadata without duplicating entries.

Optional: enable `Preferences ▸ Advanced ▸ Database ▸ Auto-relocate missing files` by pointing it to `~/Music/DJ`.

## 2. Intelligent Playlists

Create once; rekordbox refreshes rules automatically.

| Playlist | Rule | Purpose |
|----------|------|---------|
| `Stems – Vocals` | `Comments` contains `STEM=VOCALS` | Shows all vocal stems. |
| `Stems – Drums` | `Comments` contains `STEM=DRUMS`. |
| `Warmup 100-110` | `BPM` between `100` and `110`, `My Tag` contains `Warmup`. |
| `Harmonic 8A` | `Musical Key` equals `8A` (Camelot). |

Use rekordbox My Tags to store energy, venue, or status (e.g., `To Test`).

## 3. Track Separation + DDJ-FLX4

Although only the DDJ-FLX10 has dedicated hardware buttons, the FLX4 can control Track Separation via MIDI Learn:

1. `Preferences ▸ Controller ▸ MIDI`.
2. Click **Import** → choose `docs/assets/midi/track-sep-flx4.csv` (create later) or map manually:
   - Assign Pad Layer 3 (Sampler) buttons 1–3 to `VOCALS`, `INSTRUMENT`, `DRUMS` toggles.
   - Optionally map Shift+Pads to `Isolate` commands.
3. Enable `Track Separation` in `Preferences ▸ Extensions`.
4. Press the mapped pads to toggle components while a track plays. Visual stems waveform appears above the deck.

## 4. rekordbox Cloud / USB Export

- Sync with rekordbox Cloud Library Sync if you use multiple machines.
- For USB export (CDJ use):
  1. Insert formatted drive (FAT32/ExFAT).
  2. Right-click playlist > `Export to <USB>`.
  3. After export, run `docs/workflows/usb-export.md` checksums.

## 5. Using Offline Stems

- Load `Artist - Title (Instrumental)` on Deck 1 (create by combining stems if desired).
- Load `Artist - Title [VOCALS].wav` on Deck 2.
- Alternatively, add stems to rekordbox Sampler slots for finger-drumming via FLX4 pads.

## 6. Analysis

- rekordbox analyses BPM/Key on import. If you plan to trust your own analysis, disable `Preferences ▸ Analysis ▸ Beatgrid` auto-run and manually update comment/fields.
- Rekordbox writes results back into tags when you choose `Update Collection` (good for other apps).

## 7. Troubleshooting

| Issue | Solution |
|-------|----------|
| Stems not found | Ensure Comments include `STEM=` and that Intelligent Playlist rule matches. Reload tags (`Right-click ▸ Reload Tags`). |
| Track Separation missing | Update to rekordbox 7+, ensure you are in Performance mode (not Export). |
| FLX4 controls unresponsive | Check MIDI mode (shift+deck 4-beat button). Reset mapping via MIDI panel. |
| Missing audio on USB | Run `File ▸ Display Missing Files` to relink before exporting; verify with checksum script in docs. |

Review Pioneer release notes each quarter—rekordbox updates sometimes reset MIDI assignments.
