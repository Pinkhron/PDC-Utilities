import os
import json
import platform

from discord import app_commands
import discord

from dotenv import load_dotenv

# Load ENV

load_dotenv()
TOKEN = os.getenv('TOKEN')

# JSON

with open('./json/server.json') as s:
    server = json.load(s)

with open('./json/responses.json') as res:
    responses = json.load(res)

with open('./json/assets.json') as a:
    assets = json.load(a)


class Data:
    GUILD_ID = server['guild_id']

    VERSION = assets['version']
    LOGO_BOT = assets['icons']['bot']
    LOGO_DEFAULT = assets['icons']['default']

    SHIP_LOAD = responses['ship_load']
    BALL_RESPONSE = responses['8ball_response']
    FOOTER = responses['footer']


# Initialize client

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print('Successfully logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author.bot:  # Doesn't respond to bots
        return

    if message.content.lower() == 'pdc':  # Respond to PDC
        await message.reply('is awesome', mention_author=False)

    if client.user.mentioned_in(message) and len(client.user.mention) == len(message.content):  # Mention embed
        version = Data.VERSION

        _mention = discord.Embed(title=f'\U0001F44B Hey, {message.author.name}#{message.author.discriminator}!',
                                 description='PDC Utilities is an open-source bot made by <@597178180176052234> to '
                                             'make managing PDC easier. Run `>help` for a list of commands. '
                                             'PDC Utilities was made with Python '
                                             '& Discord.py\n\n'
                                             f'- [Python](https://python.org) | v{platform.python_version()}\n'
                                             f'- [Discord.py](https://github.com/Rapptz/discord.py) | v{discord.__version__}\n'
                                             f'- [PDC Utilities](https://github.com/Pinkhron/PDC-Utilities) | v{version}\n'
                                             f'[PinkhronNetwork Status](https://status.pinkhron.net)\n\n'
                                             'Thank you for joining PDC!')
        _mention.set_thumbnail(url=Data.LOGO_DEFAULT)
        _mention.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)

        await message.reply(embed=_mention)

# Initiate (/) commands



# Run bot

client.run(TOKEN)
