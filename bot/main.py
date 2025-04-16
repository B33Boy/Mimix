import logging
from typing import AsyncGenerator

import discord
from discord import Message
from discord.ext import commands
from discord.ext.commands import Context

from bot.config import DISCORD_TOKEN, MAX_RESP_SIZE, PREFIX, VALID_USERS
from bot.logger import configure_logging
from bot.ollama import process_prompt

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
            await message.channel.send(response[i : i + MAX_RESP_SIZE])
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
async def on_ready() -> None:
    logging.info(f"Logged in as {client.user}")


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
async def scrape(ctx: Context, *args) -> None:
    if ctx.author.name not in VALID_USERS:
        return
    
    target_users: tuple[str] = args
    if not target_users:
        return
    
    async for msg in get_messages_from_channel(ctx, NUM_MESSAGES, target_users):
        logging.info(msg) # save to db


if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
