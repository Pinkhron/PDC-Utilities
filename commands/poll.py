from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from data import Data


class Poll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description='Cast a poll')
    async def poll(self, interaction: discord.Interaction, option1: str, option2: str):
        numbers = [992671851450990703, 992671853229391872, 992671854366035998, 992671855347503194, 992671856383496232]
        options = [option1, option2]

        poll = await interaction.response.send_message(embed=discord.Embed(
            title=':tada: Poll',
            description=f'<:{self.bot.get_emoji(numbers[0]).name}:{numbers[0]}>: {option1}\n'
                        f'<:{self.bot.get_emoji(numbers[1]).name}:{numbers[1]}>: {option2}'
        ).set_footer(text=Data.NAME, icon_url=Data.ICON).set_author(name=f'{interaction.user.name}#{interaction.user.discriminator}', icon_url=interaction.user.display_avatar))

        for i in range(len(options)):
            poll.add_reaction(f'<:PDC_{str(i)}:{numbers[i]}>')


async def setup(bot: commands.Bot):
    await bot.add_cog(Poll(bot), guild=discord.Object(id=Data.GUILD_ID))
