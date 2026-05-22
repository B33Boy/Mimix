import logging
from typing import AsyncGenerator

import chromadb
import discord
from discord import Message
from discord.ext import commands
from discord.ext.commands import Context

from bot.config import DISCORD_TOKEN, MAX_RESP_SIZE, PREFIX, VALID_USERS
from bot.db import get_style_samples, init_db, save_messages
from bot.logger import configure_logging
from bot.ollama import process_prompt
from bot.style import build_style_prompt

# ==================================================== Setup ====================================================
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=PREFIX, intents=intents)
configure_logging()

LIMIT = 1000  # Total number of messages to search
NUM_MESSAGES = 20  # Number of messages we want to collect

# ==================================================== Helpers ====================================================


async def validate_users(message: Message) -> bool:
    """Allow only certain users to respond

    Args:
        message (discord.Message): Discord message object
    """
    if message.author == client.user:
        return False

    if message.author.name not in VALID_USERS:
        await message.channel.send("Nah I'm not tryna reply to your bih ahh")
        return False

    return True


async def send_response(message: Message, response: str) -> None:
    """Handles sending response back to discord

    Args:
        message (discord.Message): Discord message object
        response (str): The generated response to send
    """

    if len(response) > MAX_RESP_SIZE:
        for i in range(0, len(response), MAX_RESP_SIZE):
            await message.channel.send(response[i: i + MAX_RESP_SIZE])
    else:
        await message.channel.send(response)


async def get_messages_from_channel(ctx: Context, num_messages: int, authors: tuple[str]) -> AsyncGenerator[str, None]:
    counter = 0
    async for msg in ctx.channel.history(limit=LIMIT, oldest_first=False):
        if not authors or msg.author.name in authors:
            counter += 1
            yield f" {msg.author.name} - {counter} - {msg.content}"

        if counter >= num_messages:
            return


async def command_registered(message: Message) -> bool:

    ctx: Context = await client.get_context(message)
    return ctx.command is not None


# ==================================================== Events ====================================================
@client.event
async def on_message(message: Message) -> None:
    """Handle high level message handling

    Args:
        message (discord.Message): Discord message object
    """

    if await command_registered(message):
        await client.process_commands(message)
        return

    if message.content.startswith(PREFIX):
        if await validate_users(message):
            prompt = message.content[len(PREFIX):].strip()
            if not prompt:
                await message.reply("damn, bro's not even sending a question")
                return

            async with message.channel.typing():
                response = await process_prompt(prompt)
                await send_response(message, response)


@client.command()
async def push(ctx: Context, *args) -> None:
    if ctx.author.name not in VALID_USERS:
        return

    client = await chromadb.AsyncHttpClient(host='vectordb', port=8000)
    collection = await client.get_or_create_collection("test")

    await collection.add(
        documents=["lorem ipsum...", "doc2", "doc3"],
        metadatas=[{"chapter": "3", "verse": "16"}, {
            "chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}],
        ids=["id1", "id2", "id3"]
    )


@client.event
async def on_ready():
    init_db()
    logging.info(f"Logged in as {client.user}")


@client.command()
async def scrape(ctx: Context, *target_users: str) -> None:
    """Scrape and persist messages: !scrape username1 username2"""
    if ctx.author.name not in VALID_USERS:
        return
    if not target_users:
        await ctx.send("Usage: !scrape <username> [username2 ...]")
        return

    collected = []
    async for msg in ctx.channel.history(limit=LIMIT, oldest_first=False):
        if msg.author.name in target_users and msg.content.strip():
            collected.append({
                "author": msg.author.name,
                "content": msg.content,
                "channel": str(ctx.channel),
                "timestamp": str(msg.created_at),
            })

    save_messages(collected)
    await ctx.send(f"Scraped {len(collected)} messages from {', '.join(target_users)}")


@client.command()
async def imitate(ctx: Context, target_user: str, *, prompt: str) -> None:
    """Imitate a user: !imitate username <your message>"""
    if ctx.author.name not in VALID_USERS:
        return

    samples = get_style_samples(target_user, k=20)
    if not samples:
        await ctx.send(f"No messages found for {target_user}. Run !scrape first.")
        return

    system = build_style_prompt(target_user, samples)
    async with ctx.typing():
        response = await process_prompt(prompt, system=system)
        await send_response(ctx.message, response)

if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
