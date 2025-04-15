import discord

# Hacky fix to load the .env before the config
from dotenv import load_dotenv

load_dotenv()

from bot.config import DISCORD_TOKEN  # noqa: E402

# ========================= Setup =========================
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

client = discord.Client(intents=intents)

LIMIT = 1000  # Total number of messages to search
NUM_MESSAGES = 10  # Number of messages we want to collect
AUTHORS = ["LlamaBot"]  # Messages with only these usernames will be read

# ========================= Helpers =========================


async def get_messages_from_channel(message, num_messages, authors=[], channel_name='general'):
    channel = discord.utils.get(message.guild.text_channels, name=channel_name)
    counter = 0

    async for msg in channel.history(limit=LIMIT, oldest_first=False):
        if not authors or msg.author.name in authors:
            counter += 1
            yield msg.content

        if counter >= num_messages:
            return

# ========================= Events =========================


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    async for msg in get_messages_from_channel(message, NUM_MESSAGES, authors=AUTHORS):
        print(msg)


client.run(DISCORD_TOKEN)
