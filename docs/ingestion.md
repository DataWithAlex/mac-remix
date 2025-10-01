# Ingestion Workflow (`djprep ingest`)

Updated: 28 Sep 2025.

## Purpose

- Normalise filenames and place music into `Tracks/`.
- Pull artist/title from ID3 tags (Mutagen) or CLI overrides.
- Create/append to `config/library-manifest.json` for auditing.
- Stage files for subsequent stems, analysis, and exports.

## Supported Formats

| Extension | Notes |
|-----------|-------|
| `.mp3` | Primary target; 320 kbps recommended. |
| `.wav`, `.flac`, `.aiff`, `.m4a` | Supported for ingest; some features (tag inferencing) vary by codec. |

## CLI Usage

```bash
# Basic copy (preserves source)
djprep ingest ~/Downloads/new/*.mp3

# Move instead of copy
djprep ingest ~/Downloads/new/*.mp3 --move

# Override artist/title for a single file
djprep ingest "~/Downloads/Unknown.mp3" --artist "DJ Example" --title "Sunrise Edit"

# Custom config path
djprep ingest ~/Downloads/new/*.mp3 --config ~/custom/djprep.yaml
```

### Behaviour

1. **Discovery**: Accepts individual files or directories; recurses into subfolders.
2. **Tag inference**: If Mutagen is installed and the file has ID3 tags, the CLI uses the first `artist` + `title` values. Overrides take precedence.
3. **Sanitisation**: Removes filesystem-unfriendly characters, collapses whitespace.
4. **Copy or move**: Default is copy; `--move` removes originals after a successful transfer.
5. **Manifest update**: Appends JSON entry with source, destination, metadata, timestamp.

## Post-Ingest Checklist

1. **Validate** manifest: `djprep show-manifest`.
2. **Check duplicates**: Use `jq` or spreadsheet on `library-manifest.json` to identify repeated titles.
3. **Tag enrichment** (planned for v0.2): run `djprep analyze` to populate BPM/Key.
4. **SC/Intelligent playlists**: Launch Serato/rekordbox, confirm Smart Crates / Intelligent Playlists auto-fill (rules stored in `docs/integration/*`).

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| File skipped | Unsupported extension or directory empty | Ensure files end in `.mp3/.wav` etc. Directories must contain supported formats. |
| Artist/Title blank | Missing ID3 tags or Mutagen not installed | Install Mutagen (already dependency) or use `--artist/--title`. |
| Duplicate filenames | Two tracks share artist/title | Append descriptor via `--title "Track (VIP)"` or rename source before ingesting. |
| Manifest unreadable | Manual edits corrupted JSON | Delete or fix the JSON, re-run ingest (entries will re-append). |

## Automation Ideas

- Watch folder: Use `launchd` or Hazel to call `djprep ingest` when files hit `~/Downloads/ToIngest`.
- Bulk metadata: After ingest, run a Python notebook against `library-manifest.json` for advanced tagging (energy, mood, etc.).
- GitHub Actions: Not recommended for audio (size), but you can lint docs/CLI whenever docs change.
