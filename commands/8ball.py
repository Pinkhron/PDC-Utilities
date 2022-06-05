import asyncio
import random
import os

import discord

from main import bot, Data

# File config

random.seed(os.urandom(64))

# Embeds

_loadEmbed = discord.Embed(description=':8ball: Shaking the magic 8-ball...', color=0x000000)


# Slash command

@bot.tree.command(guild=discord.Object(id=Data.GUILD_ID), name='8ball',
              description='Ask the magic 8-ball a question and it will provide you with a randomized response')
async def _8ball(interaction: discord.Interaction, *, question: str):
    if len(question) > 2048:
        return

    # Command Embed

    _responseEmbed = discord.Embed(title=':8ball: The magic 8-ball has chosen..',
                                   description=f'**Response:**  **Question:**\n'
                                               f'```{random.choice(Data.BALL_RESPONSE)}``` ```{question}```',
                                   color=0x000000)
    _responseEmbed.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)

    m = await interaction.response.send_message(embed=_loadEmbed)
    await asyncio.sleep(2.5)
    await m.edit(embed=_responseEmbed)


# Discord.py setup

def setup():
    bot.tree.add_command(_8ball)
