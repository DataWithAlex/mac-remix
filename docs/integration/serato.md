# Serato DJ Integration (DDJ-FLX4)

_Status as of 28 Sep 2025: Serato DJ Lite/Pro 3.2.1._

## 1. Library Import

1. Launch Serato DJ Lite/Pro.
2. In the Files panel, browse to `~/Music/DJ/Tracks`.
3. Drag the folder into the **All** crate; Serato creates a crate mirroring the folder.
4. Repeat for `~/Music/DJ/Stems` if you want stems as standalone tracks.

Serato remembers folder pointers; new files appear after you click **Files ▸ Rescan ID3 Tags**.

## 2. Smart Crates

Create Smart Crates once—Serato updates them automatically.

| Crate Name | Rule | Purpose |
|------------|------|---------|
| `Stems – Vocals` | `Comment` contains `STEM=VOCALS` | Lists all vocal stems. |
| `Stems – Drums` | `Comment` contains `STEM=DRUMS` | Drum-only stems. |
| `Energy 7+` | `Comment` contains `ENERGY=7` or `8` or `9` | Optional energy tagging. |
| `House 124-128` | `BPM` is between `124` and `128` AND `Genre` contains `House` | Auto-curates playable BPM range. |

The CLI will write comment tags in a later release; meanwhile, use Mixed In Key or manual tagging to add `STEM=...` comments.

## 3. DDJ-FLX4 Setup

1. Connect DDJ-FLX4 via USB-C.
2. Serato auto-switches audio to the controller (verify in Setup ▸ Audio).
3. In `Setup ▸ DJ Preferences`:
   - Enable **Replace Sampler with Stems** (Lite) or **Replace Pad Mode with Stems** (Pro).
   - Optional: set Pad Mode to **Hot Cue** when not in Stems mode.
4. Press the chosen pad mode button on the controller; pads light up for Vocal/Melody/Bass/Drums.

Pads 1–4 toggle stems, pads 5–8 engage Stem FX (Pro only). Use Smart Fader + Smart CFX toggles for creative transitions.

## 4. Using Offline Stems

- Load full track on Deck 1.
- Load `Artist - Title [VOCALS].wav` on Deck 2.
- Sync tempos; use filter/FX to blend.
- Alternatively, assign stems to the Sampler (Slot 1 Vocals, Slot 2 Drums, etc.) and trigger via pads.

## 5. Analysis Workflow

- Serato autocalculates BPM/Key when you load a track; to pre-analyse, right-click the crate ▸ **Analyze Files**.
- If you run your own BPM/Key tagging, click **Analyze Files** with only **Set Auto Gain** unchecked to avoid overwriting.

## 6. Exporting for Other Computers

- Copy `~/Music/DJ` (Tracks/Stems/Playlists) and the `~/Music/_Serato_` folder to the target machine.
- Use `Relocate Lost Files` in Serato to reconnect if drive letters differ.

## 7. Troubleshooting

| Issue | Fix |
|-------|-----|
| Stems pads do not light | Ensure Serato 3.2+; toggle pad mode. If still off, reinstall Serato and reset MIDI mapping. |
| Smart Crates empty | Confirm `Comment` tags exist (view in Serato column). Use `Files ▸ Rescan ID3 Tags`. |
| Audio dropouts | Increase USB buffer in Setup ▸ Audio, avoid USB hubs, close other audio apps. |
| DDJ-FLX4 not recognised | Use different USB cable/port. On macOS, grant Serato microphone permissions (System Settings ▸ Privacy & Security ▸ Microphone). |

Revisit this doc quarterly to align with Serato release notes.
