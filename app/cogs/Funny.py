import discord
from discord.ext import commands
from discord import app_commands


class Funny(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="egirl", description="Acts appropriately.")
    async def egirl(self, interaction: discord.Interaction):
        await interaction.response.send_message(content="Bark bark!")


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Funny(client))
