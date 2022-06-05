import asyncio
import random
import os

from discord import app_commands
import discord


# File config

random.seed(os.urandom(64))

# Embeds

_loadEmbed = discord.Embed(description=':8ball: Shaking the magic 8-ball...', color=0x000000)


# Slash command

@app_commands.command(name='8ball',
              description='Ask the magic 8-ball a question and it will provide you with a randomized response')
async def _8ball(interaction: discord.Interaction, question: str):
    if len(question) > 2048:
        return

    # Command Embed

    _responseEmbed = discord.Embed(title=':8ball: The magic 8-ball has chosen..',
                                   description=f'**Response:**  **Question:**\n'
                                               f'```{random.choice(Data.BALL_RESPONSE)}``` ```{question}```',
                                   color=0x000000)
    _responseEmbed.set_footer(text='test')

    m = await interaction.response.send_message(embed=_loadEmbed)
    await asyncio.sleep(2.5)
    await m.edit(embed=_responseEmbed)


# Discord.py setup

def setup(bot):
    bot.tree.add_command(_8ball)
