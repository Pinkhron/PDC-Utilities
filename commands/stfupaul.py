import discord
from discord import app_commands
from discord.ext import commands

from data import Data


class StfuPaul(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='stfupaul', description='tell paul to be quiet')
    async def paul(self, interaction: discord.Interaction):
        await interaction.response.send_message(content='stfu <@!237239078058328064>')


async def setup(bot: commands.Bot):
    await bot.add_cog(StfuPaul(bot), guild=discord.Object(id=Data.GUILD_ID))
