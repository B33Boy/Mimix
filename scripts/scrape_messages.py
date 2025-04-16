import logging
from typing import AsyncGenerator

import discord
from discord.ext import commands
from discord.ext.commands import Context

# Hacky fix to load the .env before the config
from dotenv import load_dotenv

from bot.logger import configure_logging

load_dotenv()

from bot.config import DISCORD_TOKEN, PREFIX, VALID_USERS  # noqa: E402

# ========================= Setup =========================
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix=PREFIX, intents=intents)
configure_logging()

LIMIT = 1000  # Total number of messages to search
NUM_MESSAGES = 10  # Number of messages we want to collect
AUTHORS = ["Mimix"]  # Messages with only these usernames will be read


# ========================= Helpers =========================
async def get_messages_from_channel(ctx: Context, num_messages: int, authors: tuple[str] = []) -> AsyncGenerator[str, None]:
    counter = 0
    async for msg in ctx.channel.history(limit=LIMIT, oldest_first=False):
        if not authors or msg.author.name in authors:
            counter += 1
            yield f" {msg.author.name} - {counter} - {msg.content}"

        if counter >= num_messages:
            return

# ========================= Events =========================
@client.command()
async def scrape(ctx: commands.Context) -> None:
    if ctx.author.name not in VALID_USERS:
        return

    async for msg in get_messages_from_channel(ctx, NUM_MESSAGES, AUTHORS):
        logging.info(msg)


client.run(DISCORD_TOKEN)
