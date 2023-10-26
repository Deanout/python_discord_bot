import nextcord as discord
from nextcord.ext import commands
import os
from dotenv import load_dotenv
import responses  # Assuming you have a 'responses.py' file


class DiscordBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.load_environment_variables()

    @staticmethod
    def load_environment_variables():
        load_dotenv()

    def collect_cogs(self):
        extensions = []
        for filename in os.listdir("./app/cogs"):
            if filename.endswith(".py"):
                extensions.append(f"app.cogs.{filename[:-3]}")
        return extensions

    def register_cogs(self):
        for extension in self.collect_cogs():
            self.load_extension(extension)

    def run_bot(self):
        self.token = os.getenv("DISCORD_TOKEN")
        self.run(self.token)

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")
        guild_id = int(os.getenv("DISCORD_GUILD_ID"))
        guild = self.get_guild(guild_id)
        self.register_cogs()

        await guild.sync_application_commands()
        print(f"Connected to guild: {guild.name} (id: {guild.id})")
