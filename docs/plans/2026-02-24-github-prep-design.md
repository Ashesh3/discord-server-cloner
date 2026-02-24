# GitHub Preparation Design

## Goal

Prepare the Discord Server Cloner repo for public GitHub release.

## Files to Add

- **README.md** — Title, features, prerequisites, installation, usage walkthrough, what gets cloned vs not, disclaimer, license
- **LICENSE** — MIT, copyright 2026 Ashesh3
- **.gitignore** — Python standard ignores plus utils/config.json (contains user token)

## Files to Remove

- `.replit` — Replit execution config
- `replit.nix` — Replit Nix environment
- `VENV.md` — Replit migration notice
- `pyproject.toml` — Stale Poetry config (wrong name/author, removed deps)
- `poetry.lock` — Stale lock file
- `.breakpoints` — Empty debug file
- `docs/plans/` — Internal dev planning docs

## README Structure

1. Title + one-line description
2. Features (what gets cloned)
3. Prerequisites (Python 3.8+, Discord account, dev mode)
4. Installation (clone, pip install, run)
5. Usage walkthrough (token, settings, server IDs)
6. What gets cloned / what doesn't (table)
7. Disclaimer (selfbot/ToS warning)
8. License (MIT)

## Out of Scope

- Badges, screenshots, contributing guide
- CI/CD setup
- Docker support
