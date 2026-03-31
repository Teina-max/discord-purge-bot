import os

import discord
from dotenv import load_dotenv

load_dotenv()

bot = discord.Bot(intents=discord.Intents.default())


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.slash_command(name="purge", description="Delete messages from the channel")
@discord.guild_only()
@discord.default_permissions(manage_messages=True)
async def purge(
    ctx: discord.ApplicationContext,
    limit: discord.Option(
        int,
        name="limit",
        description="Number of messages to scan and delete (1-100)",
        min_value=1,
        max_value=100,
        required=True,
    ),
    user: discord.Option(
        discord.User,
        name="user",
        description="Only delete messages from this user",
        required=False,
    ) = None,
):
    await ctx.defer(ephemeral=True)

    check = (lambda m: m.author == user) if user else None

    try:
        deleted = await ctx.channel.purge(
            limit=limit,
            check=check,
            reason=f"Purge by {ctx.author}",
        )
    except discord.Forbidden:
        await ctx.respond(
            "I don't have permission to delete messages in this channel.",
            ephemeral=True,
        )
        return
    except discord.HTTPException as e:
        await ctx.respond(f"Failed to purge messages: {e}", ephemeral=True)
        return

    target = f" from {user.display_name}" if user else ""
    await ctx.respond(f"Deleted {len(deleted)} message(s){target}.", ephemeral=True)


token = os.getenv("DISCORD_TOKEN")
if not token:
    raise RuntimeError("DISCORD_TOKEN environment variable is not set")

bot.run(token)
