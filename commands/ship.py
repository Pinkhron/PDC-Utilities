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

_load = discord.Embed(description=f'💗 {random.choice(Data.SHIP_LOAD)}...', color=0xFF0000)
_drumroll = discord.Embed(description='🥁 Drumroll please...', color=0xFF0000)


# Slash command

class Ship(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def setup_hook(self):
        await self.bot.tree.sync(guild=discord.Object(id=Data.GUILD_ID))

    @app_commands.command(name='ship', description='Ships two users together with a randomized percentage')
    @app_commands.guilds(discord.Object(id=Data.GUILD_ID))
    async def _ship(self, interaction: discord.Interaction, usr1: discord.Member, usr2: discord.Member):
        score = random.randint(0, 100)

        def text_score(num):
            if num in range(100, 101):
                return 'What an amazing pair :heart_eyes:'
            elif num in range(90, 100):
                return ':heart_on_fire: Sheesh, what a high score.'
            elif num in range(80, 90):
                return ':heart: I think they are.. in love..'
            elif num in range(65, 80):
                return 'This relationship\'s outcome seems promising..'
            elif num in range(50, 65):
                return 'Eh, it\'s a start'
            elif num in range(35, 50):
                return ':fire: With a little magic, you can make this into a reality'
            elif num in range(10, 35):
                return ':rolling_eyes: Idk man, maybe it\'s time to find someone else..'
            elif num in range(0, 10):
                return ':rofl: HAHA Keep living a fantasy there buddy'

        def heart_score(num):
            if num in range(90, 101):
                return ':heartpulse:'
            elif num in range(80, 90):
                return ':sparkling_heart:'
            elif num in range(70, 80):
                return ':revolving_hearts:'
            elif num in range(50, 70):
                return ':heart:'
            elif num in range(35, 50):
                return ':broken_heart:'
            elif num in range(0, 35):
                return ':black_heart:'

        # Command embeds

        _result = discord.Embed(title=':heartpulse: I rate this ship a...',
                                      description=f'{text_score(score)}\n\n'
                                                  f'{usr1.mention} < {heart_score(score)} > {usr2.mention}\n\n'
                                                  f'**Score:** {score}%',
                                color=0xFF0000)
        _result.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)

        await interaction.response.send_message(embed=_load)
        await asyncio.sleep(1.5)
        await interaction.edit_original_message(embed=_drumroll)
        await asyncio.sleep(1.5)
        await interaction.edit_original_message(embed=_result)


# Discord.py setup

async def setup(bot: commands.Bot):
    await bot.add_cog(Ship(bot))
