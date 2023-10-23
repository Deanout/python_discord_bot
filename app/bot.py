import discord
import responses
from dotenv import load_dotenv
import os


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)
        await message.channel.send("Sorry, I don't understand you.")


def run_discord_bot():
    # Get the token from ../.env
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    guilds = []
    for guild in client.guilds:
        guilds.append(guild.name)
    print(f"Connected to guilds: {guilds}")

    @client.event
    async def on_ready():
        print(f"{client.user} has connected to Discord!")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith("!"):
            await send_message(message, message.content, False)
        else:
            await send_message(message, message.content, True)

    client.run(token)
