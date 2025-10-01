# Folder Structure & Naming Conventions

Reference date: 28 Sep 2025.

## Base Layout

```
~/Music/DJ/
├── Tracks/
│   └── Artist - Title (Mix Info).ext
├── Stems/
│   └── Artist - Title/
│       ├── Artist - Title [VOCALS].wav
│       ├── Artist - Title [DRUMS].wav
│       ├── Artist - Title [BASS].wav
│       └── Artist - Title [OTHER].wav
└── Playlists/
    ├── Stems - Vocals.m3u
    └── Club - House 124-128.m3u
```

## Naming Rules

- **Tracks**: `Artist - Title (Descriptor).ext`
  - `Descriptor` optional (e.g., `Extended Mix`, `Live Edit`).
  - Use camel-case for descriptors, avoid special characters.
- **Stems**: Keep original artist/title, append `[STEMTYPE]` in square brackets.
  - Valid values: `VOCALS`, `DRUMS`, `BASS`, `OTHER`, `PIANO`, etc. (expand as needed).
- **Playlists**: Short descriptive phrases; keep spaces (Serato/rekordbox handle them fine).

## Metadata Mapping

| Field | Where stored | Why |
|-------|--------------|-----|
| BPM (`TBPM`) | ID3 tag (Mutagen) / Rekordbox analysis | Drives Smart/Intelligent playlists. |
| Key (`TKEY`/`initialkey`) | ID3 tag or comment | Harmony sorting; convert to Camelot if desired. |
| Comment | e.g. `STEM=VOCALS`, `ENERGY=7`, `SOURCE=Bandcamp` | Serato Smart Crates parse this easily. |
| Grouping/MyTag | Optional; rekordbox supports My Tags, Serato uses Smart Crate columns. |

## Path Hygiene

- Avoid nested artist folders. Flat `Tracks/` keeps import simple and matches Rekordbox XML expectations.
- Keep stems inside their own folder to make mass-deletes safe (`rm -rf Stems/Artist - Title`).
- Git ignores audio automatically (see `.gitignore`) so you can work without committing large files.

## Manifest

- Every ingest adds an object to `config/library-manifest.json`:
  ```json
  {
    "source": "/Users/.../Downloads/Track.mp3",
    "library_path": "/Users/.../Music/DJ/Tracks/Artist - Title.mp3",
    "artist": "Artist",
    "title": "Title",
    "ingested_at": "2025-09-28T12:15:04"
  }
  ```
- Use `djprep show-manifest` to audit.
- The manifest doubles as a dataset for building Smart Crates or detecting duplicates.

## Backups & Sync

- Mirror `~/Music/DJ` to an external SSD before shows.
- If using iCloud, ensure `Optimize Mac Storage` is **disabled** for the DJ folder so files stay local.
- Keep `config/` and `docs/` under version control (this repo) for reproducibility.
