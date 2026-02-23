# Discord Server Cloner - Bugfix & Cleanup Design

## Scope

Fix all 6 identified bugs (4 critical, 2 moderate) and clean up dead code, unused dependencies, and unused config keys. Stay on discord.py 1.7.3.

## Changes by File

### main.py

**Import/startup (critical bug #4):**
- Remove try/except wrapper around imports. Import normally at the top.
- If dependencies are missing, print "Missing dependencies. Run: pip install -r requirements.txt" and sys.exit(1).
- Remove useless version check (`if discord.__version__ != "1.7.3": pass`).
- Remove bare try/except around Client() creation; let it crash with a real traceback.

**Token handling (critical bug #1, moderate bug #5):**
- When user enters a new token: prompt "Save token for next time?" and if yes, persist via edit_config("token", self.TOKEN).
- When token is found in config: assign self.TOKEN = self.data["token"].
- On invalid token exception: write the cleared token back to config.json, not just in-memory.

**Stale settings (critical bug #2):**
- Remove module-level config load (line 27-28).
- In clone_server(), reload config from config.json at function start.

**Guild validation (critical bug #3):**
- After get_guild() calls, check for None.
- If either guild is None, print error message and return early.

**Client failure (moderate bug #6):**
- Remove bare try/except around Client creation. A failure here should halt the program.

### utils/cloner.py

**Dead code (quality #9):**
- Fix logs() function: the if/else branches are identical except for clear_line(). Clean up the branching logic.

### utils/config.json

**Unused keys (quality #9):**
- Remove "prefix": "!" (never read).
- Remove "permissions": true (never read).

### requirements.txt

**Unused/duplicate deps (quality #7, #8):**
- Remove discord==1.7.3 (duplicate of discord.py==1.7.3).
- Remove psutil==5.9.0 (unused).
- Remove pypresence==4.2.1 (unused).
- Add rich (used by panel.py but missing).

## Out of Scope

- Upgrading to discord.py 2.x
- Adding new features (message backup, role member associations, etc.)
- Changing the selfbot approach (bot=False)
