from app.cogs.Help import MyHelpCommand
from app.client import Client
import discord
from discord.ext import commands
from app.database.adapter import Sqlite3Adapter


def main():
    print("Starting bot...")

    # Create database
    db = Sqlite3Adapter("app/database/dev.db")

    # Create client
    client = Client(db)
    client.help_command = MyHelpCommand()

    @client.tree.command(name="reload", description="Reloads all cogs")
    async def reload(interaction: discord.Interaction):
        for ext in client.cogslist:
            await client.reload_extension(ext)
        await interaction.response.send_message(content="Reloaded all cogs!")

    client.run(client.token)


if __name__ == "__main__":
    main()
