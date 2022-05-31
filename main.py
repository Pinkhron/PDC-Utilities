import os
import json
import time
import platform
import random

from discord.ext.commands import has_role
from discord.ext import commands
import discord

from dotenv import load_dotenv

# Load ENV

load_dotenv()
TOKEN = os.getenv('TOKEN')

# Config

with open('config.json') as cfg:
    config = json.load(cfg)

guild_id = config["bot"]["server_id"]
logo2 = config["bot"]["icons"]["logo2"]
general = config["server"]["general"]
member_role = config["roles"]["member"]
vc_global = config["server"]["vc_global"]

_footer = 'Made with \u2764\uFE0F by Pinkhron | \u00a9 PDC Utilities 20220'

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
    if message.author.bot:  # Doesn't respond to bots
        return

    if bot.user.mentioned_in(message):  # Mention embed
        version = config["bot"]["version"]

        _mention = discord.Embed(title=f"\U0001F44B Hey, <@!{message.author.id}>!",
                                 description="PDC Utilities is an open-source bot made by <@597178180176052234> to "
                                             "make managing PDC easier. PDC Utilities was made with Python "
                                             "& Discord.py\n\n"
                                             f"- [Python](https://python.org) | v{platform.python_version()}\n"
                                             f"- [Discord.py](https://github.com/Rapptz/discord.py) | v{discord.__version__}\n"
                                             f"- [PDC Utilities](https://github.com/Pinkhron/PDC-Utilities) | v{version}\n"
                                             f"[PinkhronNetwork Status](https://status.pinkhron.net)\n \n"
                                             "Thank you for joining PDC!")
        _mention.set_thumbnail(url=config["bot"]["icons"]["confetti"])
        _mention.set_footer(text=_footer, icon_url=logo2)

        await message.reply(embed=_mention)

    if message.content.lower() == "pdc":  # Respond to PDC
        await message.reply("is awesome", mention_author=False)

    await bot.process_commands(message)

"""
@bot.event
async def on_member_join(member):
    _general = bot.get_channel(general)

    _join = discord.Embed(title="A new member has joined PDC!", description="{} has joined PDC."
                                                                            "They have been invited by ".format(member))
    _join.set_footer(text=_footer, icon_url=logo2)

    await _general.send(embed=_join)
"""
# Bot commands


@bot.command(name='ping')
async def _ping(ctx):
    await ctx.reply("\U0001F3D3 Responded in `{0}ms`.".format(round(bot.latency * 1000)))


@bot.command(name='8ball')
async def _8ball(ctx, *, question):
    responses = ["Yes!", "Sure.", "Ok", "Positive", "Hell yeah", "Is that even a no",
                 "No.", "Nah", "Hell no.", "In your dreams", "No chance", "Negative",
                 "Idk", "hmm", "Ask again later, I'm too lazy rn", "Really?", "HAHAHAHAHAHA"]

    _loading = discord.Embed(color=0x000000,
                             description='\U0001F3B1 Shaking the magic 8-ball...')

    _response = discord.Embed(title='\U0001F3B1 The magic 8-ball has spoken..',
                              description=f"**User:** <@!{ctx.author.id}>\n"
                              f"**Response:** {random.choice(responses)}\n"
                              f"**Question Asked:** {str(question)}",
                              color=0x000000)
    _response.set_footer(text=_footer, icon_url=logo2)

    m = await ctx.reply(embed=_loading, mention_author=False)
    time.sleep(2.5)
    await m.edit(embed=_response)

# Music


@bot.command(name='join')
@has_role(member_role)
async def _join(ctx):
    if not ctx.message.author.voice:
        await ctx.reply("❌ You need to join a voice channel to run this command")
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()
    await ctx.reply(f"Successfully connected to {channel}!")
    await ctx.message.add_reaction("<a:PDC_Success:981093316114399252")

# Run bot

bot.run(TOKEN)
