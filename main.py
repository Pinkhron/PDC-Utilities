import os
import json

from discord.ext.commands import has_role, MissingRole
from discord.ext import commands
import discord

from dotenv import load_dotenv

# Load ENV

load_dotenv()
TOKEN = os.getenv('TOKEN')

# Config file

with open('server.json') as cfg:
    config = json.load(cfg)

# Initialize client

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='>', intents=intents)


@bot.event
async def on_ready():
    print('Successfully logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == "pdc":
        await message.reply('is awesome', mention_author=True)


# Run bot

bot.run(TOKEN)
