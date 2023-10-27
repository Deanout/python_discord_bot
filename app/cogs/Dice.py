# Discord Cog that responds to /roll commands.
import discord
from discord.ext import commands
from discord import app_commands
import random


class Dice(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="d6", description="Rolls a die!")
    async def d6(self, interaction: discord.Interaction):
        result = random.randint(1, 6)
        await interaction.response.send_message(content="You rolled a " + str(result))

    # Roll a die with a specified number of sides
    @app_commands.command(name="roll", description="Rolls a die!")
    async def roll(self, interaction: discord.Interaction, sides: int):
        """
        Rolls a die with a specified number of sides.

        Args:
          sides (int): The number of sides the die has.
        """
        result = random.randint(1, sides)
        await interaction.response.send_message(content="You rolled a " + str(result))

    # Roll a die with a specified number of sides and a specified number of times
    @app_commands.command(name="roll_n", description="Rolls a die n times!")
    async def roll_n(self, interaction: discord.Interaction, sides: int, times: int):
        """
        Rolls a die with a specified number of sides and a specified number of times.

        Args:
          sides (int): The number of sides the die has.
          times (int): The number of times to roll the die.
        """
        results = []
        for _ in range(times):
            results.append(random.randint(1, sides))
        await interaction.response.send_message(content="You rolled " + str(results))

    # Roll a die with a specified number of sides and a specified number of times, and add a modifier
    @app_commands.command(
        name="roll_n_modifier", description="Rolls a die n times and adds a modifier!"
    )
    async def roll_n_modifier(
        self, interaction: discord.Interaction, sides: int, times: int, modifier: int
    ):
        """
        Rolls a die with a specified number of sides and a specified number of times, and add a modifier.

        Args:
          sides (int): The number of sides the die has.
          times (int): The number of times to roll the die.
          modifier (int): The modifier to add to the result of the roll.
        """
        results = []
        for _ in range(times):
            results.append(random.randint(1, sides))
        await interaction.response.send_message(
            content=f"You rolled a d{sides} {times} times and added {modifier} to get {sum(results) + modifier}!"
        )

    # Roll a die with a specified number of sides and specify the result because it's a rigged roll.
    @app_commands.command(name="roll", description="Rolls a die!")
    async def roll(
        self, interaction: discord.Interaction, sides: int, result: int = None
    ):
        """
        Rolls a die with a specified number of sides and specify the result because it's a rigged roll.

        Args:
          sides (int): The number of sides the die has.
          result (int): The result of the roll.
        """
        if result is None:
            result = random.randint(1, sides)
        await interaction.response.send_message(
            content=f"You rolled a d{sides} and got {result}!"
        )


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Dice(client))
