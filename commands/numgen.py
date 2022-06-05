import random
import os

import discord

from main import tree, Data

# File config

random.seed(os.urandom(64))


# Slash command

@tree.command(guild=discord.Object(id=Data.GUILD_ID), name='numgen',
              description='Generates a random number')
async def _numgen(interaction: discord.Interaction, num1: int, num2: int):
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

def setup():
    tree.add_command(_numgen)
