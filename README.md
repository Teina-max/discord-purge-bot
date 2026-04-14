# discord-purge-bot

Py-cord Discord bot with `/purge` command for bulk message deletion.

**Requires Python 3.10+**

## How it works

- Registers a `/purge` slash command visible only to users with **Manage Messages** permission
- Deletes messages in batches of 100 with a 1-second delay between batches to respect Discord rate limits
- Checks both bot and user permissions before acting — if the command targets another channel, the user must have Manage Messages there too
- All responses are ephemeral (only visible to the command author)
- Supports optional filters: target a specific user or channel

## Setup

### 1. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to **Bot** tab, copy the token
4. Go to **OAuth2 > URL Generator**, select scopes: `bot`, `applications.commands`
5. Select permissions: `Manage Messages`, `Read Message History`
6. Use the generated URL to invite the bot to your server

### 2. Install & Run

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set your DISCORD_TOKEN
python bot.py
```

## Usage

| Command | Description |
|---------|-------------|
| `/purge limit:50` | Delete the last 50 messages |
| `/purge limit:200` | Delete 200 messages (batched automatically) |
| `/purge limit:10 user:@someone` | Delete the last 10 messages from a specific user |
| `/purge limit:100 channel:#general` | Delete 100 messages in a specific channel |

- `limit`: Number of messages to delete (1-500, batched in groups of 100)
- `user`: Optional filter — only delete messages from this user
- `channel`: Optional target channel (defaults to current channel)

The command is only visible to users with **Manage Messages** permission.
The bot needs **Manage Messages** and **Read Message History** permissions in the target channel.
