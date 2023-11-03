import discord
from discord.ext import commands
from discord import app_commands
from app.models.server_list import ServerList


class CommunityServer(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    # Returns an embed list of all the community servers.
    # A community server contains: a name, a game, an IP Address, a port, and a description.
    @app_commands.command(
        name="server_list", description="Sends details on the community servers!"
    )
    async def server_list(self, interaction: discord.Interaction):
        # Acknowledge the interaction first
        await interaction.response.send_message(
            "Sending server list...", ephemeral=True
        )

        servers = self.get_server_list()

        for server in servers:
            embed = self.server_info_embed(server)
            await interaction.followup.send(embed=embed)

    def server_info_embed(self, server):
        """Generates embed object for server info"""
        text = self.create_server_text(server)
        embed = discord.Embed(title=f"Server: {server[1]}", color=0x00FF00)
        embed.add_field(name="Details", value=text, inline=False)
        embed.set_image(url=server[6])

        return embed

    def get_server_list(self):
        # Get server info from the DB.
        server_list = ServerList(self.client.db)
        servers = server_list.all()
        return servers

    def server_embed(self, server):
        """Generates embed object for server"""
        text = self.create_server_text(server)
        embed = discord.Embed(title="Server Info", color=0x00FF00)
        embed.add_field(name="Server Info", value=text, inline=False)
        embed.set_image(url=server[6])
        return embed

    def create_server_text(self, server):
        id = server[0]
        name = server[1]
        game = server[2]
        description = server[3]
        ip = server[4]
        port = server[5]

        return (
            f"**Name:** {name} \n"
            f"**Game:** {game} \n"
            f"**Description:** {description} \n"
            f"**IP:** {ip} \n"
            f"**Port:** {port} \n"
            f"**ID:** {id} \n"
        )

    # Create a community server.
    @app_commands.command(
        name="create_server", description="Creates a community server!"
    )
    async def create_server(
        self,
        interaction: discord.Interaction,
        server_name: str,
        game_name: str,
        ip_address: str,
        port: str,
        server_description: str = None,
        image: discord.Attachment = None,
    ):
        image_url = ""
        # Get attachments from the interaction.
        if image is not None:
            image_url = image.url

        # Create a community server using the server_list model.
        community_server = ServerList(self.client.db)
        community_server.create(
            server_name, game_name, ip_address, port, server_description, image_url
        )

        await interaction.response.send_message(content="Created a community server!")

    # Deletes a community server by ID.
    @app_commands.command(
        name="delete_server", description="Deletes a community server!"
    )
    async def delete_server(self, interaction: discord.Interaction, id: str):
        # Create a community server using the server_list model.
        community_server = ServerList(self.client.db)
        community_server.delete(id)

        await interaction.response.send_message(content="Deleted a community server!")

    # Updates a community server by ID.
    @app_commands.command(
        name="update_server", description="Updates a community server!"
    )
    async def update_server(
        self,
        interaction: discord.Interaction,
        id: str,
        server_name: str,
        game_name: str,
        ip_address: str,
        port: str,
        server_description: str = None,
    ):
        # Create a community server using the server_list model.
        community_server = ServerList(self.client.db)
        community_server.update(
            id, server_name, game_name, ip_address, port, server_description
        )

        await interaction.response.send_message(content="Updated a community server!")

    # Returns a community server by ID.
    @app_commands.command(
        name="server_info", description="Returns a community server by ID!"
    )
    async def server_info(self, interaction: discord.Interaction, id: str):
        # Create a community server using the server_list model.
        community_server = ServerList(self.client.db)
        server = community_server.find(id=id)
        if server is None:
            await interaction.response.send_message(
                content="Couldn't find a community server with that ID!"
            )
            return

        embed = self.server_embed(server)
        await interaction.response.send_message(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(CommunityServer(client))
