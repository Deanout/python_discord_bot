import nextcord as discord
from nextcord.ext import commands
import os
from dotenv import load_dotenv
import responses  # Assuming you have a 'responses.py' file

# Create a bot instance with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="/")


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

    # Register guild by the ID in the env file.
    guild_id = int(os.getenv("DISCORD_GUILD_ID"))
    guild = bot.get_guild(guild_id)
    print(f"Connected to guild: {guild.name} (id: {guild.id})")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    is_private = not message.guild  # Checks if the message is from a guild or not

    if is_private:
        await message.channel.send(responses.handle_response(message.content))
    elif message.content.startswith("/"):
        await bot.process_commands(message)


@bot.slash_command(
    name="hello",
    description="Say hello!",
    # Add your command options and settings here if needed
)
async def hello(interaction: discord.Interaction):
    await interaction.send("Hello, World!")


# Callback SlashApplicationCommand ping is missing the interaction parameter
@bot.slash_command(
    name="ping",
    description="Ping the bot to see if it's alive.",
    # Add your command options and settings here if needed
)
async def ping(interaction: discord.Interaction):
    """Ping the bot to see if it's alive."""
    await interaction.send("Pong!")


# Function to run the Discord bot, which you'll call from main.py
def run_discord_bot():
    load_dotenv()  # Load environment variables from .env file
    token = os.getenv("DISCORD_TOKEN")  # Get token from .env
    bot.run(token)  # Run the bot
