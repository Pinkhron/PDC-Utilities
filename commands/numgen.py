import random
import os

from discord import app_commands
from discord.ext import commands
import discord

from data import Data

# File config

random.seed(os.urandom(64))


# Slash command

class Numgen(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def setup_hook(self):
        await self.bot.tree.sync(guild=discord.Object(id=Data.GUILD_ID))

    @app_commands.command( name='numgen', description='Generates a random number')
    @app_commands.guilds(discord.Object(id=Data.GUILD_ID))
    async def _numgen(self, interaction: discord.Interaction, num1: int, num2: int):
        if num1 > num2:
            await interaction.response.send_message(discord.Embed(description=':x: `<num1>` cannot be higher than `<num2>`'))
            return
        elif (num1 > 1e24) or (num2 > 1e24):
            await interaction.response.send_message(discord.Embed(description=':x: Number(s) cannot be over a septillion'))
            return

        # Command embed

        _result = discord.Embed(title=':game_die: Number generated!', description=f'```{random.randint(num1, num2)}```')
        _result.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)

        await interaction.response.send_message(embed=_result)


# Discord.py setup

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Numgen(bot))
