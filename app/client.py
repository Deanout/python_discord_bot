import discord
from discord.ext import commands
from colorama import Back, Fore, Style
import os
import platform
import time
from dotenv import load_dotenv


class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents().default()
        intents.message_content = True
        super().__init__(
            command_prefix=commands.when_mentioned_or("."), intents=intents
        )
        self.cogslist = self.load_cogs()
        self.load_environment_variables()
        self.token = os.getenv("DISCORD_TOKEN")
        self.guild_id = os.getenv("DISCORD_GUILD_ID")

    @staticmethod
    def load_environment_variables():
        load_dotenv()

    def load_cogs(self):
        loaded_cogs = []
        for filename in os.listdir("./app/cogs"):
            if filename.endswith(".py"):
                loaded_cogs.append("app.cogs." + filename[:-3])
        return loaded_cogs

    async def setup_hook(self):
        for ext in self.cogslist:
            await self.load_extension(ext)

    async def on_ready(self):
        prefix = (
            Back.BLACK
            + Fore.GREEN
            + time.strftime("%H:%M:%S UTC", time.gmtime())
            + Back.RESET
            + Fore.WHITE
            + Style.BRIGHT
        )
        print(prefix + " Logged in as " + Fore.YELLOW + self.user.name)
        print(prefix + " Bot ID " + Fore.YELLOW + str(self.user.id))
        print(prefix + " Discord Version " + Fore.YELLOW + discord.__version__)
        print(
            prefix + " Python Version " + Fore.YELLOW + str(platform.python_version())
        )
        synced = await self.tree.sync()
        print(
            prefix
            + " Slash CMDs Synced "
            + Fore.YELLOW
            + str(len(synced))
            + " Commands"
        )
