import nextcord
from app import responses
from nextcord.ext import commands
import os
from dotenv import load_dotenv


class BasicCommand(commands.Cog):
    guild_id = os.getenv("DISCORD_GUILD_ID")

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="hello",
        description="Say hello!",
        guild_ids=[guild_id],
    )
    async def hello(self, interaction: nextcord.Interaction):
        await interaction.send("Hello, World!")

    @commands.command(
        name="ping",
        description="Ping the bot to see if it's alive.",
        guild_ids=[guild_id],
    )
    async def ping(self, interaction: nextcord.Interaction):
        await interaction.send("Pong!")

    @commands.command(
        name="roll",
        description="Roll a dice.",
        guild_ids=[guild_id],
    )
    async def roll(self, interaction: nextcord.Interaction):
        await interaction.send(responses.handle_response("roll"))


def setup(bot):
    bot.add_cog(BasicCommand(bot))
