# Discord Server Cloner

Clone a Discord server's structure — roles, channels, categories, and emojis — to another server.

<img width="507" height="972" alt="image" src="https://github.com/user-attachments/assets/600bb91e-99e9-468f-8b54-3c29e5ac9683" />


## Features

- Server name and icon
- Roles with permissions, colors, and hoist status
- Categories with permission overwrites
- Text channels (topic, NSFW, slowmode delay)
- Voice channels (bitrate, user limit)
- Custom emojis
- Configurable — choose what to clone

## Prerequisites

- Python 3.8 or higher
- A Discord account that is a member of both the source and destination servers
- Developer Mode enabled in Discord (Settings > Advanced > Developer Mode)

## Installation

```bash
git clone https://github.com/Ashesh3/discord-server-cloner.git
cd discord-server-cloner
pip install -r requirements.txt
cp utils/config.example.json utils/config.json
```

## Usage

1. Run `python main.py`
2. Enter your Discord token when prompted
3. Choose whether to edit clone settings (roles, channels, categories, emojis)
4. Enter the **destination** server ID — create an empty server first, as all existing channels will be deleted
5. Enter the **source** server ID — the server you want to clone from
6. The tool connects and clones automatically

> To get a server ID: enable Developer Mode in Discord settings, then right-click a server name and select "Copy Server ID".

## What Gets Cloned

| Cloned | Not Cloned |
|--------|------------|
| Server name & icon | Messages |
| Roles (permissions, colors, hoist) | Member list |
| Categories (with overwrites) | Role assignments |
| Text channels (topic, NSFW, slowmode) | Bans |
| Voice channels (bitrate, user limit) | Webhooks |
| Custom emojis | Integrations |
| Permission overwrites | Boost status / Stickers |

## Disclaimer

> **Warning:** This tool uses a user account token (selfbot), which violates Discord's Terms of Service. Your account may be suspended or terminated. Use at your own risk. The destination server's existing channels are deleted before cloning begins.

## License

MIT License — see [LICENSE](LICENSE) for details.
