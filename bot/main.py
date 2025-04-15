import logging

import discord

from bot.config import DISCORD_TOKEN, MAX_RESP_SIZE, PREFIX, VALID_USERS
from bot.logger import configure_logging
from bot.ollama import query_ollama

# ==================================================== Setup ====================================================
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
configure_logging()


# ==================================================== Helpers ====================================================
async def validate_users(message) -> bool:
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


async def send_response(message, response: str) -> None:
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


# ==================================================== Events ====================================================
@client.event
async def on_ready():
    logging.info(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    """Handle high level message handling

    Args:
        message (discord.Message): Discord message object
    """
    if await validate_users(message):
        if message.content.startswith(PREFIX):
            prompt = message.content[len(PREFIX) :].strip()
            if not prompt:
                await message.reply("damn, bro's not even sending a question")
                return

            async with message.channel.typing():
                response = await query_ollama(prompt)
                await send_response(message, response)



if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
