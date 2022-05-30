import os
import json
import time
import platform
import random

import discord
from discord import app_commands

from dotenv import load_dotenv

# Load ENV

load_dotenv()
TOKEN = os.getenv('TOKEN')

# Config file

with open('config.json') as cfg:
    config = json.load(cfg)

guild_id = config["bot"]["server_id"]
logo2 = config["bot"]["icons"]["logo2"]

# Initialize client

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True


class Bot(discord.Client):
    async def startup(self):
        await self.wait_until_ready()
        await tree.sync(guild=discord.Object(id=guild_id))


client = Bot(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print("Successfully logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if client.user.mentioned_in(message):
        version = config["bot"]["version"]

        _mention = discord.Embed(title=f"\U0001F44B Hey, <@!{message.author.id}>!",
                                    description="PDC Utilities is an open-source bot made by <@597178180176052234> to "
                                                "make managing PDC easier. PDC Utilities was made with Python "
                                                "& Discord.py\n\n"
                                                f"- [Python](https://python.org) | v{platform.python_version()}\n"
                                                f"- [Discord.py](https://github.com/Rapptz/discord.py) | v{discord.__version__}\n"
                                                f"- [PDC Utilities](https://github.com/Pinkhron/PDC-Utilities) | v{version}")
        _mention.set_thumbnail(url=config["bot"]["icons"]["confetti"])
        _mention.set_footer(text="Made with \u2764\uFE0F by Pinkhron | \u00a9 PDC Utilities 2022",
                               icon_url=logo2)

        await message.reply(embed=_mention)

    if message.content.lower() == "pdc":
        await message.reply("is awesome", mention_author=True)

# Slash commands


@tree.command(guild=discord.Object(id=guild_id), name='8ball', description='Ask question get random response')
async def _8ball(interaction: discord.Interaction, message: discord.Message):
    responses = ["Yes!", "Sure.", "Ok", "Positive", "Hell yeah", "Is that even a no"
                 "No.", "Nah", "Hell no.", "In your dreams", "No chance", "Negative"
                 "Idk", "hmm", "Ask again later, I'm too lazy rn", "Really?", "HAHAHAHAHAHA"]

    _loading = discord.Embed(color=0x000000,
                             description='<a:PDC_Loading:980936150065750036> Shaking the magic 8-ball...')

    _response = discord.Embed(title='\U0001F3B1 The magic 8-ball has spoken..',
                              description=f"**User:** <@!{message.author.id}>\n"
                              f"**Response:** {random.choice(responses)}\n"
                              f"**Question Asked:**",
                              color=0x000000)
    _response.set_footer(text="Made with \u2764\uFE0F by Pinkhron | \u00a9 PDC Utilities 2022",
                         icon_url=logo2)

    await interaction.response.send_message(embed=_loading)
    time.sleep(2.5)
    await interaction.response.edit_message(embed=_response)


# Run bot

client.run(TOKEN)
