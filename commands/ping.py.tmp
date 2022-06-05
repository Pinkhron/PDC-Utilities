from discord import app_commands
from discord.ext import commands
import discord

from data import Data

# Embed

_pingEmbed = discord.Embed(title=':ping_pong: Pong!', description=f'```{round(bot.latency * 1000)}ms```')
_pingEmbed.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)


# Slash Command

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='ping', description='Tests the ping between Discord and PDC Utilities')
    async def _ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=_pingEmbed)


# Discord.py setup

async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))
