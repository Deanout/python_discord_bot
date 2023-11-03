# docker exec docker-mc-1 rcon-cli

import discord
from discord.ext import commands
from discord import app_commands
import subprocess


# This is a Minecraft server cog.
# Used to manage a minecraft server running on the host machine
# as a docker-compose service.
# Also includes a rcon-cli command to send commands to the server.
class Minecraft(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(
        name="start_minecraft_server", description="Starts the Minecraft server!"
    )
    async def start_minecraft_server(self, interaction: discord.Interaction):
        await interaction.response.send_message(content="Starting Minecraft server!")
        # Run docker-compose up -d on the host machine.
        # This will start the Minecraft server.

        self.start_docker_compose_server("./app/assets/docker/docker-compose.yml")

    @app_commands.command(
        name="stop_minecraft_server", description="Stops the Minecraft server!"
    )
    async def stop_minecraft_server(self, interaction: discord.Interaction):
        await interaction.response.send_message(content="Stopping Minecraft server!")
        # Run docker-compose down on the host machine.
        # This will stop the Minecraft server.

        self.stop_docker_compose_server("./app/assets/docker/docker-compose.yml")

    @app_commands.command(
        name="rcon_cli", description="Sends a command to the Minecraft server!"
    )
    async def rcon_cli(
        self, interaction: discord.Interaction, service_name: str, command: str
    ):
        await interaction.response.send_message(content="Sending command to server!")
        # Run docker-compose exec -T <service_name> rcon-cli <command> on the host machine.
        # This will send the command to the Minecraft server.

        self.run_docker_compose_command(service_name, command)

    @app_commands.command(
        name="restart_minecraft_server", description="Restarts the Minecraft server!"
    )
    async def restart_minecraft_server(self, interaction: discord.Interaction):
        await interaction.response.send_message(content="Restarting Minecraft server!")
        # Run docker-compose down on the host machine.
        # This will stop the Minecraft server.
        self.stop_docker_compose_server("./app/assets/docker/docker-compose.yml")

        # Run docker-compose up -d on the host machine.
        # This will start the Minecraft server.
        self.start_docker_compose_server("./app/assets/docker/docker-compose.yml")

    @app_commands.command(
        name="minecraft_server_status",
        description="Returns the status of the Minecraft server!",
    )
    async def minecraft_server_status(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            content="Checking Minecraft server status!"
        )
        # Run docker-compose ps on the host machine.
        # This will return the status of the Minecraft server.
        status = await self.check_docker_compose_server_status(
            "./app/assets/docker/docker-compose.yml"
        )
        # Reply with the status of the Minecraft server.
        await interaction.followup.send(content=status)

    def run_docker_compose_command(self, service_name, command):
        # Command to be executed, for example 'docker-compose exec -T <service_name> <command>'
        compose_command = [
            "docker-compose",
            "exec",
            "-T",
            service_name,
            "rcon-cli",
            command,
        ]

        # Running the docker-compose command
        process = subprocess.run(
            compose_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Check if the command was successful
        if process.returncode == 0:
            print(f"Success: {process.stdout}")
        else:
            print(f"Error: {process.stderr}")

    def start_docker_compose_server(self, compose_file_path):
        # Command to start the server
        compose_up_command = ["docker-compose", "-f", compose_file_path, "up", "-d"]

        # Running the docker-compose command
        process = subprocess.run(
            compose_up_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Check if the command was successful
        if process.returncode == 0:
            print(f"Server is starting: {process.stdout}")
        else:
            print(f"Error starting the server: {process.stderr}")

    def stop_docker_compose_server(self, compose_file_path):
        # Command to stop the server
        compose_down_command = ["docker-compose", "-f", compose_file_path, "down"]

        # Running the docker-compose command
        process = subprocess.run(
            compose_down_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Check if the command was successful
        if process.returncode == 0:
            print(f"Server is stopping: {process.stdout}")
        else:
            print(f"Error stopping the server: {process.stderr}")

    async def check_docker_compose_server_status(self, compose_file_path):
        # Command to check the server status
        compose_ps_command = ["docker-compose", "-f", compose_file_path, "ps"]

        # Running the docker-compose command
        process = subprocess.run(
            compose_ps_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Check if the command was successful
        if process.returncode == 0:
            print(f"Server status: {process.stdout}")
            # Get the up time of the server located in the STATUS column
            status = self.parse_status(process.stdout)
            return status

        else:
            print(f"Error checking the server status: {process.stderr}")
            return process.stderr

    def parse_status(self, output):
        # Split the output by lines
        lines = output.strip().split("\n")
        # Find the line with the status info
        for line in lines:
            if "Up" in line:
                # Extract the status part, which is after the 'CREATED' and before 'PORTS' column
                parts = line.split()
                # Find the index for 'Up'
                up_index = parts.index("Up")
                # The status is two parts, 'Up' and the time '2 minutes'.
                status = " ".join(parts[up_index : up_index + 3])
                return status
        return "Server offline"


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Minecraft(client))
