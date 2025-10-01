# Ingestion Workflow (Action Sheet)

Use alongside `docs/ingestion.md`. This version is condensed for quick reference during sessions.

1. **Stage files** in `~/Downloads/ToIngest`.
2. **Activate virtualenv**: `source /path/to/.venv/bin/activate`.
3. **Copy or move**:
   ```bash
   djprep ingest ~/Downloads/ToIngest --move
   ```
4. **Verify manifest**: `djprep show-manifest`.
5. **Tag check**: Ensure Artist/Title populated; edit in Serato/rekordbox if missing.
6. **Clear staging**: Confirm folder empty before closing terminal.
7. **Log**: Note any issues in Git commit or personal changelog.

For edge cases (unknown tags, duplicates, etc.), see `docs/ingestion.md`.
