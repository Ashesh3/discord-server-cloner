# Discord Server Cloner Bugfix & Cleanup Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix 6 bugs and clean up dead code/unused dependencies in the Discord Server Cloner.

**Architecture:** Direct fixes to existing files. No new files, no new abstractions. Four files touched: main.py, utils/cloner.py, utils/config.json, requirements.txt.

**Tech Stack:** Python 3.8+, discord.py 1.7.3, rich, colorama

---

### Task 1: Clean up requirements.txt and config.json

**Files:**
- Modify: `requirements.txt`
- Modify: `utils/config.json`

**Step 1: Edit requirements.txt**

Remove unused and duplicate packages, add missing `rich` dependency:

```
discord.py==1.7.3
colorama==0.4.4
rich
```

**Step 2: Edit utils/config.json**

Remove unused `prefix` and `permissions` keys:

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

**Step 3: Verify JSON is valid**

Run: `python -c "import json; json.load(open('utils/config.json'))"`
Expected: No output (no error)

**Step 4: Commit**

```bash
git add requirements.txt utils/config.json
git commit -m "chore: remove unused deps and config keys"
```

---

### Task 2: Fix import/startup flow in main.py

**Files:**
- Modify: `main.py:1-30`

**Step 1: Replace the try/except import block and module-level config load**

Replace lines 1-30 with clean imports and a dependency check:

```python
import subprocess
import os
import sys
import json
import time

try:
    import discord
    from discord import Client, Intents
    from rich.prompt import Prompt, Confirm
    from colorama import Fore, Style
except ImportError:
    print("Missing dependencies. Run: pip install -r requirements.txt")
    sys.exit(1)

from utils.cloner import Cloner
from utils.panel import Panel, Panel_Run
from time import sleep

client = Client(intents=Intents.all())

os.system('cls' if os.name == 'nt' else 'clear')
```

Key changes:
- Specific `ImportError` instead of bare `except Exception`
- Print instructions and exit instead of auto-install
- Remove useless version check
- Remove bare try/except around Client()
- Remove module-level config.json load (fixes stale settings bug)

**Step 2: Verify syntax**

Run: `python -c "import ast; ast.parse(open('main.py').read()); print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add main.py
git commit -m "fix: clean up import/startup flow in main.py"
```

---

### Task 3: Fix token handling in ClonerBot

**Files:**
- Modify: `main.py` — `ClonerBot.main()` method (around lines 101-123 after Task 2 edits)

**Step 1: Fix the main() method**

Replace the `main()` method with this corrected version:

```python
  def main(self):
    self.clear()
    if self.data["token"] == False:
      self.TOKEN = Prompt.ask("\n> Enter your Token")
      save_token = Confirm.ask("> Save token for next time?")
      if save_token:
        self.edit_config("token", self.TOKEN)
      sleep(0.5)
    else:
      self.TOKEN = self.data["token"]
      print("> Token Found")
    self.clear()
    edit_settings = Confirm.ask("\n> Do you want to edit the settings?")
    self.clear()
    if edit_settings:
      self.edit_settings_function()
    self.clear()

    self.GUILD = Prompt.ask(
        '\n> Enter the Server ID you want to edit (Create a Server Manually)')
    sleep(0.5)

    self.INPUT_GUILD_ID = Prompt.ask(
        "\n> Enter the Server ID you want to copy from")
    sleep(0.5)

    return self.INPUT_GUILD_ID, self.TOKEN, self.GUILD
```

Key changes:
- Save token to config when user opts in
- Load token from config when it exists (`self.TOKEN = self.data["token"]`)
- Fix typo "Manully" -> "Manually"

**Step 2: Verify syntax**

Run: `python -c "import ast; ast.parse(open('main.py').read()); print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add main.py
git commit -m "fix: token handling - save and load correctly"
```

---

### Task 4: Fix clone_server() — stale settings and null guild checks

**Files:**
- Modify: `main.py` — `clone_server()` function

**Step 1: Replace clone_server() with fixed version**

```python
async def clone_server():
  with open("./utils/config.json", "r") as json_file:
    data = json.load(json_file)

  start_time = time.time()
  guild_from = client.get_guild(int(INPUT_GUILD_ID))
  guild_to = client.get_guild(int(GUILD))

  if guild_from is None:
    print(f"\n> Error: Could not find source server with ID {INPUT_GUILD_ID}.")
    print("> Make sure this account is a member of that server.")
    return
  if guild_to is None:
    print(f"\n> Error: Could not find destination server with ID {GUILD}.")
    print("> Make sure this account is a member of that server.")
    return

  print(" ")

  await Cloner.guild_create(guild_to, guild_from)
  await Cloner.channels_delete(guild_to)

  if data["copy_settings"]["roles"]:
    await Cloner.roles_create(guild_to, guild_from)
  if data["copy_settings"]["categories"]:
    await Cloner.categories_create(guild_to, guild_from)
  if data["copy_settings"]["channels"]:
    await Cloner.channels_create(guild_to, guild_from)
  if data["copy_settings"]["emojis"]:
    await Cloner.emojis_create(guild_to, guild_from)

  print("\n> Done Cloning Server in " +
        str(round(time.time() - start_time, 2)) + " seconds")
```

Key changes:
- Reload config from file at function start (fixes stale settings)
- Check both guilds for None before proceeding
- Clear error messages when guild not found

**Step 2: Verify syntax**

Run: `python -c "import ast; ast.parse(open('main.py').read()); print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add main.py
git commit -m "fix: reload config in clone_server and validate guild IDs"
```

---

### Task 5: Fix error handler to persist config

**Files:**
- Modify: `main.py` — the `if __name__ == "__main__"` block at the bottom

**Step 1: Replace the bottom block**

```python
if __name__ == "__main__":
  INPUT_GUILD_ID, TOKEN, GUILD = ClonerBot().main()
  try:
    client.run(TOKEN, bot=False)
    clear()
  except Exception as e:
    print(e)
    print("> Invalid Token")
    with open("./utils/config.json", "r") as f:
      data = json.load(f)
    data["token"] = False
    with open("./utils/config.json", "w") as f:
      json.dump(data, f, indent=4)
```

Key change: Actually write the cleared token back to config.json on failure.

**Step 2: Verify syntax**

Run: `python -c "import ast; ast.parse(open('main.py').read()); print('OK')"`
Expected: `OK`

**Step 3: Commit**

```bash
git add main.py
git commit -m "fix: persist token reset to config on auth failure"
```

---

### Task 6: Fix dead code in utils/cloner.py logs()

**Files:**
- Modify: `utils/cloner.py:18-32`

**Step 1: Fix the logs() function**

Replace with cleaner version where the branching actually does something different:

```python
def logs(message, type, is_summary=False):
  if logs_enabled:
    log_types = {
      'add': ('[+]', Fore.GREEN),
      'delete': ('[-]', Fore.RED),
      'warning': ('[WARNING]', Fore.YELLOW),
      'error': ('[ERROR]', Fore.RED)
    }
    prefix, color = log_types.get(type, ('[?]', Fore.RESET))
    print(f" {color}{prefix}{Style.RESET_ALL} {message}")
    if not is_summary:
      clear_line()
```

Key changes:
- Rename `number` parameter to `is_summary` (clearer intent: summary lines stay visible, per-item lines get cleared)
- Remove duplicate print statement
- Single print, conditional clear_line()

**Step 2: Update all callers**

The callers already pass `True` as the third argument for summary lines (e.g., `logs(f"Created Roles: {roles_created}", 'add', True)`). The parameter name change is internal only — no caller changes needed since it's positional.

**Step 3: Verify syntax**

Run: `python -c "import ast; ast.parse(open('utils/cloner.py').read()); print('OK')"`
Expected: `OK`

**Step 4: Commit**

```bash
git add utils/cloner.py
git commit -m "fix: clean up dead branch in logs() function"
```

---

### Task 7: Final verification

**Step 1: Verify all files parse correctly**

Run: `python -c "import ast; ast.parse(open('main.py').read()); ast.parse(open('utils/cloner.py').read()); ast.parse(open('utils/panel.py').read()); import json; json.load(open('utils/config.json')); print('All files OK')"`
Expected: `All files OK`

**Step 2: Review the full diff**

Run: `git diff HEAD~7..HEAD --stat` to confirm only the expected files changed.

---
