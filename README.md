# discord-purge-bot

Py-cord Discord bot with `/purge` command for bulk message deletion.

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
| `/purge limit:10 user:@someone` | Delete the last 10 messages from a specific user |

- `limit`: Number of messages to delete (1-100)
- `user`: Optional filter — only delete messages from this user

The command is only visible to users with **Manage Messages** permission.
