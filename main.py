import os
import json
import platform

from discord.ext.commands import has_role, MissingRole
from discord.ext import commands
import discord

from dotenv import load_dotenv

# Load ENV

load_dotenv()
TOKEN = os.getenv('TOKEN')

# Config file

with open('config.json') as cfg:
    config = json.load(cfg)

# Initialize client

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='>', intents=intents)


@bot.event
async def on_ready():
    print("Successfully logged in as {0.user}".format(bot))


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if bot.user.mentioned_in(message):
        v = config["bot"]["version"]

        ping_embed = discord.Embed(title=f"PDC Utilities v{v}", url="https://github.com/Pinkhron/PDC-Utilities",
                                   description="PDC Utilities is an open-source bot made by <@597178180176052234> to "
                                               "manage PDC easier. PDC Utilities was made with Python & Discord.py\n\n"
                                               f"- [Discord.py](https://github.com/Rapptz/discord.py) | v{discord.__version__}\n"
                                               f"- [Python](https://python.org) | v{platform.python_version()}")
        ping_embed.set_thumbnail(url=config["bot"]["icons"]["confetti"])
        ping_embed.set_footer(text="Made with \u2764\uFE0F by Pinkhron | \u00a9 PDC Utilities 2022",
                              icon_url=config["bot"]["icons"]["logo2"])

        await message.reply(embed=ping_embed)

    if message.content.lower() == "pdc":
        await message.reply("is awesome", mention_author=True)


# Run bot

bot.run(TOKEN)
