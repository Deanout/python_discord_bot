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

    @app_commands.command(name="shutdown", description="Shutdown the bot!")
    async def shutdown(self, interaction: discord.Interaction):
        await interaction.response.send_message(content="Shutting down...")
        await self.client.close()

    # Default to the user who invoked the command
    @app_commands.command(name="userinfo", description="Get user info!")
    async def userinfo(
        self, interaction: discord.Interaction = None, user: discord.User = None
    ):
        if user is None:
            user = interaction.user

        embed = discord.Embed(title="User Info", description=f"User: {user.mention}")
        embed.add_field(name="ID", value=user.id)
        embed.add_field(name="Bot", value=user.bot)
        embed.add_field(name="Created At", value=user.created_at)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="clear_channel", description="Clears the channel!")
    async def clear_channel(self, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(content="Clearing channel...")
            await interaction.channel.purge()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Admin(client))
