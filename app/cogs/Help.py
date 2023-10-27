from discord.ext import commands
from discord import app_commands


class MyHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        channel = self.get_destination()
        await channel.send("Here are all the commands you can use: ")

        for cog, cmd_list in mapping.items():
            commands_list = " ".join([command.name for command in cmd_list])
            if cog:
                cog_name = cog.qualified_name
                app_commands_list = " ".join(
                    [command.name for command in getattr(cog, "app_commands", [])]
                )
                all_commands_list = f"{commands_list} {app_commands_list}".strip()
                if all_commands_list:
                    await channel.send(
                        f"In {cog_name}, you can use: {all_commands_list}"
                    )


class HelpCog(commands.Cog):
    def __init__(self, client):
        self._original_help_command = client.help_command
        client.help_command = MyHelpCommand()
        client.help_command.cog = self

    def cog_unload(self):
        self.client.help_command = self._original_help_command


async def setup(client: commands.Bot) -> None:
    await client.add_cog(HelpCog(client))
