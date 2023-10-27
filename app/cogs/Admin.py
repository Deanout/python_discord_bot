import discord
from discord.ext import commands
from discord import app_commands


class Admin(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="admin", description="Admin Only Command!")
    async def admin(self, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(content="You're an admin!")
        else:
            await interaction.response.send_message(content="You're not an admin!")


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Admin(client))
