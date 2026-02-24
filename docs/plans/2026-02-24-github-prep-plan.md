# GitHub Preparation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Prepare the Discord Server Cloner repo for public GitHub release with README, LICENSE, .gitignore, and cleanup of Replit artifacts.

**Architecture:** Add standard GitHub project files, remove Replit-specific files and internal dev docs, ensure .gitignore protects the user's token.

**Tech Stack:** Git, Markdown

---

### Task 1: Add .gitignore

**Files:**
- Create: `.gitignore`

**Step 1: Create .gitignore**

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
*.egg-info/
dist/
build/
*.egg

# Virtual environments
venv/
.venv/
env/

# IDE
.breakpoints
.vscode/
.idea/
*.swp
*.swo

# Replit
.config/
.local/
.cache/

# User config (contains Discord token)
utils/config.json
```

**Step 2: Verify .gitignore works**

Run: `git status`
Expected: `.config/`, `.local/`, `__pycache__/`, `.breakpoints` should no longer appear as untracked.

**Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: add .gitignore

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: Add LICENSE

**Files:**
- Create: `LICENSE`

**Step 1: Create MIT LICENSE file**

Use the standard MIT license text with copyright "2026 Ashesh3".

**Step 2: Commit**

```bash
git add LICENSE
git commit -m "chore: add MIT license

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Add README.md

**Files:**
- Create: `README.md`

**Step 1: Create README.md**

Structure:
1. `# Discord Server Cloner` — title
2. One-line description: Clone a Discord server's structure (roles, channels, categories, emojis) to another server.
3. `## Features` — bullet list: server name & icon, roles with permissions/colors/hoist, categories with permission overwrites, text channels (topic, NSFW, slowmode), voice channels (bitrate, user limit), custom emojis
4. `## Prerequisites` — Python 3.8+, Discord account that is a member of both source and destination servers, Developer Mode enabled in Discord
5. `## Installation` — git clone, pip install -r requirements.txt
6. `## Usage` — step-by-step: run python main.py, enter token, configure settings, enter destination server ID (must create manually), enter source server ID, tool clones automatically. Include how to get a server ID (Developer Mode > right-click > Copy Server ID).
7. `## What Gets Cloned` — table with two columns: "Cloned" (server name/icon, roles, categories, channels, emojis, permission overwrites) and "Not Cloned" (messages, member list, role assignments, bans, webhooks, integrations, boost status, stickers)
8. `## Disclaimer` — This tool uses a user token (selfbot) which violates Discord's Terms of Service. Your account may be terminated. Use at your own risk. The destination server's channels are wiped before cloning.
9. `## License` — MIT License, link to LICENSE file

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add README with usage guide and disclaimer

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: Remove Replit files, stale configs, and internal docs

**Files:**
- Delete: `.replit`
- Delete: `replit.nix`
- Delete: `VENV.md`
- Delete: `pyproject.toml`
- Delete: `poetry.lock`
- Delete: `docs/plans/2026-02-24-bugfix-cleanup-design.md`
- Delete: `docs/plans/2026-02-24-bugfix-cleanup-plan.md`
- Delete: `docs/plans/2026-02-24-github-prep-design.md`
- Delete: `docs/` (entire directory, should be empty after above)

**Step 1: Remove all files**

```bash
git rm .replit replit.nix VENV.md pyproject.toml poetry.lock
git rm -r docs/
```

**Step 2: Verify only expected files remain**

Run: `git ls-files`
Expected files:
- `.gitignore`
- `LICENSE`
- `README.md`
- `main.py`
- `requirements.txt`
- `utils/cloner.py`
- `utils/panel.py`

Note: `utils/config.json` should NOT be tracked (it's in .gitignore). But it's currently tracked from the initial commit. We need to untrack it:

```bash
git rm --cached utils/config.json
```

But we still need users to have a config.json when they clone the repo. So we add a template:

Create `utils/config.example.json` with the default config (token: false, logs: true, all copy_settings: true). Update README installation section to mention copying config.example.json to config.json.

**Step 3: Create utils/config.example.json**

```json
{
    "token": false,
    "logs": true,
    "copy_settings": {
        "categories": true,
        "channels": true,
        "roles": true,
        "emojis": true
    }
}
```

**Step 4: Update main.py and utils/cloner.py**

Both files open `./utils/config.json`. If the file doesn't exist on first run, the tool crashes. Add a check in main.py at startup: if `utils/config.json` doesn't exist, copy from `utils/config.example.json`.

Add after the imports in main.py, before `client = Client(...)`:

```python
# Create config from template if it doesn't exist
if not os.path.exists("./utils/config.json"):
  import shutil
  shutil.copy("./utils/config.example.json", "./utils/config.json")
```

**Step 5: Commit**

```bash
git add -A
git commit -m "chore: remove Replit files and internal docs, add config template

- Remove .replit, replit.nix, VENV.md, pyproject.toml, poetry.lock
- Remove docs/plans/ internal development docs
- Untrack utils/config.json (contains user token)
- Add utils/config.example.json as template
- Auto-create config.json from template on first run

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: Final verification

**Step 1: Verify tracked files**

Run: `git ls-files`
Expected:
```
.gitignore
LICENSE
README.md
main.py
requirements.txt
utils/cloner.py
utils/config.example.json
utils/panel.py
```

**Step 2: Verify config.json is not tracked**

Run: `git ls-files utils/config.json`
Expected: no output

**Step 3: Verify syntax**

Run: `python -c "import ast; ast.parse(open('main.py').read()); print('OK')"`
Expected: `OK`

---
