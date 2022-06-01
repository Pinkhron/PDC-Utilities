import os
import json
import asyncio
import platform
import random

from discord.ext.commands import has_role
from discord.ext import commands
import discord

from pytube import YouTube
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

_footer = 'Made with \u2764\uFE0F by Pinkhron | \u00a9 PDC Utilities 2022'

# Initialize client

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or('>'), intents=intents)


@bot.event
async def on_ready():
    print("Successfully logged in as {0.user}".format(bot))


@bot.event
async def on_message(message):
    if message.author.bot:  # Doesn't respond to bots
        return

    if message.content.lower() == "pdc":  # Respond to PDC
        await message.reply("is awesome", mention_author=False)

    if bot.user.mentioned_in(message) and len(bot.user.mention) == len(message.content):  # Mention embed
        version = config["bot"]["version"]

        _mention = discord.Embed(title=f"\U0001F44B Hey, <@!{message.author.id}>!",
                                 description="PDC Utilities is an open-source bot made by <@597178180176052234> to "
                                             "make managing PDC easier. Run `>help` for a list of commands. "
                                             "PDC Utilities was made with Python "
                                             "& Discord.py\n\n"
                                             f"- [Python](https://python.org) | v{platform.python_version()}\n"
                                             f"- [Discord.py](https://github.com/Rapptz/discord.py) | v{discord.__version__}\n"
                                             f"- [PDC Utilities](https://github.com/Pinkhron/PDC-Utilities) | v{version}\n"
                                             f"[PinkhronNetwork Status](https://status.pinkhron.net)\n\n"
                                             "Thank you for joining PDC!")
        _mention.set_thumbnail(url=config["bot"]["icons"]["confetti"])
        _mention.set_footer(text=_footer, icon_url=logo2)

        await message.reply(embed=_mention)

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


@bot.command(name='ping')  # Utility
async def _ping(ctx):
    await ctx.reply("\U0001F3D3 Responded in `{0}ms`.".format(round(bot.latency * 1000)))


@bot.command(name='8ball')  # Random
async def _8ball(ctx, *, question):
    if len(question) > 2048:
        return

    responses = ["Yes!", "Sure.", "Ok", "Positive", "Hell yeah", "Is that even a no",
                 "No.", "Nah", "Hell no.", "In your dreams", "No chance", "Negative",
                 "Idk", "hmm", "Ask again later, I'm too lazy rn", "Really?", "HAHAHAHAHAHA"]

    _loading = discord.Embed(description='\U0001F3B1 Shaking the magic 8-ball...', color=0x000000)

    _response = discord.Embed(title='\U0001F3B1 The magic 8-ball has chosen..',
                              description=f"**User:** <@!{ctx.author.id}>\n"
                              f"**Response:** {random.choice(responses)}\n"
                              f"**Question Asked:** {str(question)}",
                              color=0x000000)
    _response.set_footer(text=_footer, icon_url=logo2)

    m = await ctx.reply(embed=_loading, mention_author=False)
    await asyncio.sleep(2.5)
    await m.edit(embed=_response)


@bot.command(name='ship')  # Random
async def _ship(ctx, mem1: discord.Member, mem2: discord.Member):
    score = random.randint(0, 100)

    def heart_score(num):
        if num in range(90, 101):
            return '💗'
        elif num in range(80, 90):
            return '💖'
        elif num in range(70, 80):
            return '💞'
        elif num in range(50, 70):
            return '❤'
        elif num in range(35, 50):
            return '💔'
        elif num in range(0, 35):
            return '🖤'

    _load_random = ["Reading diaries", "Reading divorce papers", "Checking finances", "Scrolling through DMs"]
    _loading = discord.Embed(description=f'💗 {random.choice(_load_random)}...', color=0xFF0000)
    _drumroll = discord.Embed(description='🥁 Drumroll please...', color=0xFF0000)

    _love = discord.Embed(title='💗 I rate this ship a...',
                          description=f'**Requester: <@!{ctx.author.id}>**\n\n'
                          f'{mem1.mention} < {heart_score(score)} > {mem2.mention}\n\n'
                          f'**Score:** {score}%',
                          color=0xFF0000)
    _love.set_footer(text=_footer, icon_url=logo2)

    m = await ctx.reply(embed=_loading, mention_author=False)
    await asyncio.sleep(1.5)
    await m.edit(embed=_drumroll)
    await asyncio.sleep(1.5)
    await m.edit(embed=_love)


@bot.command(name='numgen')  # Random
async def _numgen(ctx, num1: int, num2: int):
    if num1 > num2:
        ctx.reply("❌ First number cannot be higher than the second number.")
        return

    _result = discord.Embed(title='🎲 Number Generated!', description=f'```{random.randint(num1, num2)}```')
    _result.set_footer(text=_footer, icon_url=logo2)

    await ctx.reply(content=f'<@!{ctx.message.author.id}>', embed=_result)


# Music

"""
@bot.command(name='join')
@has_role(member_role)
async def _join(ctx):

    ctx.send("WARNING: PDC Music player is in beta. Bugs may occur & embed layout will most likely change.")

    if not ctx.message.author.voice:
        await ctx.reply("You are not connected to a voice channel")
        return
    else:
        channel = ctx.message.author.voice.channel
        await ctx.reply("Connected")
    await channel.connect()


@bot.command(name='play')
@has_role(member_role)
async def _play(ctx, link):
    mp3_path = "./mp3"
    vid = YouTube(link)

    _info = discord.Embed(title='🎵 Playing audio...', description=f'📹 **Title:** {vid.title}\n'
                                                                  f'👁️ **Views:** {vid.views}'
                                                                  f'🔥 **Author:** {vid.author}')
    _info.set_footer(text=_footer, icon_url=logo2)

    ctx.send("WARNING: PDC Music player is in beta. Bugs may occur & embed layout will most likely change.")

    if vid.length > 600:
        ctx.reply("❌ Video cannot be over 10 minutes")
        return
    else:
        vid.streams.get_audio_only().download(mp3_path)
        voice_channel = ctx.message.author.voice.channel
        
        player = voice_channel.create_ffmpeg_player()
"""

# Run bot

bot.run(TOKEN)
