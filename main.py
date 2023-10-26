from app.discord_bot import DiscordBot
from app.cogs.BasicCommand import BasicCommand
import nextcord as discord
import os


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = DiscordBot(command_prefix="/", intents=intents)
    bot.run_bot()


if __name__ == "__main__":
    main()
