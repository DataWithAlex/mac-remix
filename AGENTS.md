# AGENTS Guide

This file explains how autonomous or semi-autonomous coding agents should operate within the **mac-remix** repository. Keep it updated whenever the workflow or tooling changes.

## Environment

- Default shell: `zsh`
- Working directory: `/Users/alexsciuto/Library/Mobile Documents/com~apple~CloudDocs/DataWithAlex/mac-remix`
- Python version: 3.11+ recommended
- Virtualenv: `.venv/` (create with `python3 -m venv .venv`)

## Repository Rules

1. **Audio assets** (`*.mp3`, `*.wav`, etc.) are excluded via `.gitignore`. Never attempt to commit binaries.
2. All code lives under `src/djprep/`. Prefer Typer CLI patterns and keep modules importable.
3. Documentation lives under `docs/`; refresh timestamps (e.g., “Updated: 28 Sep 2025”) whenever you materially change content.
4. Use `requirements.txt` / `pyproject.toml` for dependency changes; ensure both stay aligned.
5. Run formatters (`ruff`, `black`) before proposing code changes.

## Git Workflow

- Branch from `main` unless instructed otherwise.
- Write conventional commit messages (`feat:`, `fix:`, `docs:`) when possible.
- Never rewrite history on `main`; use PRs or merges.

## Coding Practices

- Use Python type hints; Typer integrates well with hints for CLI help text.
- Handle missing optional dependencies gracefully (e.g., Mutagen, Demucs).
- Avoid destructive actions; when moving files, provide a `--dry-run` option.
- Log to console with Rich for consistency.

## Documentation Standards

- Keep instructions explicit with copy-pasteable commands.
- Reference absolute dates (DD Month YYYY) to avoid ambiguity.
- Surface dependencies’ minimum versions.
- Link to repo-relative files using backticks (`docs/...`). Avoid raw URLs in docs unless pointing to vendor downloads.

## Testing

- CLI smoke tests: run `python -m djprep --help` and `djprep init --dry-run` (future) before shipping.
- For features touching external binaries (Demucs, ffmpeg), document manual test steps instead of running heavy commands in CI.

## Escalations

- If instructions conflict or you encounter unexpected local changes, pause and ask the human operator for guidance before proceeding.
- For new automation (e.g., Rekordbox XML export), draft design notes in `docs/architecture.md` prior to implementation.

Maintain this document as the single source of truth for agent conduct.
