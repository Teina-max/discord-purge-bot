import asyncio
import os

import discord
from dotenv import load_dotenv

load_dotenv()

bot = discord.Bot(intents=discord.Intents.default())

BATCH_SIZE = 100
MAX_LIMIT = 500


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.slash_command(name="purge", description="Delete messages from a channel")
@discord.guild_only()
@discord.default_permissions(manage_messages=True)
async def purge(
    ctx: discord.ApplicationContext,
    limit: discord.Option(
        int,
        name="limit",
        description="Number of messages to delete (1-500)",
        min_value=1,
        max_value=MAX_LIMIT,
        required=True,
    ),
    user: discord.Option(
        discord.User,
        name="user",
        description="Only delete messages from this user",
        required=False,
    ) = None,
    channel: discord.Option(
        discord.TextChannel,
        name="channel",
        description="Target channel (defaults to current)",
        required=False,
    ) = None,
):
    await ctx.defer(ephemeral=True)

    target_channel = channel or ctx.channel

    bot_perms = target_channel.permissions_for(ctx.guild.me)
    if not bot_perms.manage_messages or not bot_perms.read_message_history:
        await ctx.edit(
            content=f"I need **Manage Messages** and **Read Message History** permissions in {target_channel.mention}."
        )
        return

    if channel:
        user_perms = target_channel.permissions_for(ctx.author)
        if not user_perms.manage_messages:
            await ctx.edit(
                content=f"You don't have **Manage Messages** permission in {target_channel.mention}."
            )
            return

    check = (lambda m: m.author == user) if user else None
    total_deleted = 0
    remaining = limit
    empty_rounds = 0

    try:
        while remaining > 0:
            batch = min(remaining, BATCH_SIZE)
            deleted = await target_channel.purge(
                limit=batch,
                check=check,
                reason=f"Purge by {ctx.author}",
            )
            count = len(deleted)
            total_deleted += count

            if check:
                remaining -= count
                if count == 0:
                    empty_rounds += 1
                    if empty_rounds >= 2:
                        break
                else:
                    empty_rounds = 0
            else:
                remaining -= batch
                if count < batch:
                    break

            if remaining > 0:
                await ctx.edit(
                    content=f"Purging... {total_deleted} message(s) deleted so far."
                )
                await asyncio.sleep(1)

    except discord.Forbidden:
        await ctx.edit(
            content=f"I don't have permission to delete messages in {target_channel.mention}."
        )
        return
    except discord.HTTPException:
        await ctx.edit(content="An error occurred while purging messages.")
        return

    target_label = f" from {user.display_name}" if user else ""
    channel_label = f" in {target_channel.mention}" if channel else ""
    await ctx.edit(
        content=f"Deleted {total_deleted} message(s){target_label}{channel_label}."
    )


token = os.getenv("DISCORD_TOKEN")
if not token:
    raise RuntimeError("DISCORD_TOKEN environment variable is not set")

bot.run(token)
