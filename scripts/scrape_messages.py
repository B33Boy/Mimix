import logging

import discord
from discord import Message
from discord.ext import commands

# Hacky fix to load the .env before the config
from dotenv import load_dotenv

load_dotenv()

from bot.config import DISCORD_TOKEN, PREFIX, VALID_USERS  # noqa: E402

# ========================= Setup =========================
intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix=PREFIX, intents=intents)

LIMIT = 1000  # Total number of messages to search
NUM_MESSAGES = 100  # Number of messages we want to collect
AUTHORS = ["LlamaBot"]  # Messages with only these usernames will be read

# ========================= Helpers =========================

async def get_messages_from_channel(ctx, num_messages, authors=[]):
    counter = 0
    async for msg in ctx.channel.history(limit=LIMIT, oldest_first=False):
        if not authors or msg.author.name in authors:
            counter += 1
            yield f" {counter} - {msg.content}"

        if counter >= num_messages:
            return

# ========================= Events =========================

@client.command()
async def test(ctx, *args):
    arguments = ', '.join(args)
    await ctx.send(f'{len(args)} arguments: {arguments}')

@client.command()
async def scrape(ctx: commands.Context):
    
    if ctx.author.name not in VALID_USERS:
        return

    async for msg in get_messages_from_channel(ctx, NUM_MESSAGES, AUTHORS):
        logging.error(msg)


client.run(DISCORD_TOKEN)
