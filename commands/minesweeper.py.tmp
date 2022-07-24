import os
import random

import discord
from discord import app_commands
from discord.ext import commands

from data import Data

# Random
random.seed(os.urandom(64))
gem = random.randint(1, 25)


# Buttons
class MinesweeperButton(discord.ui.Button):
    def __init__(self):
        super().__init__(emoji='❓', style=discord.ButtonStyle.blurple)


class MinesweeperView(discord.ui.View):
    def __init__(self):
        super().__init__()

        for i in range(25):
            self.add_item(MinesweeperButton())


# Command
class Minesweeper(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @app_commands.command(description='Play a game of minesweeper')
    async def minesweeper(self, interaction: discord.Interaction):
        view = MinesweeperView()

        await interaction.response.send_message(content=f'<@!{interaction.user.id}>', view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(Minesweeper(bot), guild=discord.Object(id=Data.GUILD_ID))
