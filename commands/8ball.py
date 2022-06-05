import asyncio
import random
import os

from discord import app_commands
from discord.ext import commands
import discord

from data import Data

# File config

random.seed(os.urandom(64))

# Embeds

_loadEmbed = discord.Embed(description=':8ball: Shaking the magic 8-ball...', color=0x000000)


# Slash command

class Ball(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def setup_hook(self):
        await self.bot.tree.sync(guild=discord.Object(id=Data.GUILD_ID))

    @app_commands.command(name='8ball',
                          description='Ask the magic 8-ball a question and it will provide you with a randomized response')
    @app_commands.guilds(discord.Object(id=Data.GUILD_ID))
    async def _8ball(self, interaction: discord.Interaction, question: str):
        if len(question) > 2048:
            return

        # Command Embed

        _responseEmbed = discord.Embed(title=':8ball: The magic 8-ball has chosen..',
                                       description=f'**Response:** {random.choice(Data.BALL_RESPONSE)}'
                                                   f'**Question:** {question}\n',
                                       color=0x000000)
        _responseEmbed.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)

        await interaction.response.send_message(embed=_loadEmbed)
        await asyncio.sleep(2.5)
        await interaction.edit_original_message(embed=_responseEmbed)


# Discord.py setup

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ball(bot))
