import os
import time
import random
import platform
from datetime import datetime

import discord
from discord.ext import commands

from dotenv import load_dotenv
from data import Data

# ENV & File settings

load_dotenv()
TOKEN = os.getenv('DISCORD')

random.seed(os.urandom(64))

# Initialize client

print(f'Starting PDC Utilities v{Data.VERSION}..')

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents, owner_id=Data.OWNER_ID)


# Bot

@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user}')

    if __name__ == '__main__':
        for cmd in os.listdir('./commands'):
            if cmd.endswith('.py'):
                await bot.load_extension(f'commands.{cmd[:-3]}')


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.lower() == 'pdc':
        await message.reply(
            content=f'is {random.choice(["epic", "awesome", "amazing", "the best", "on fire :fire:", "love", "life"])}'
        )

    if bot.user.mentioned_in(message) and len(bot.user.mention) == len(message.content):
        await message.reply(embed=discord.Embed(
            title=f':wave: Hey, {message.author.name}',
            color=Data.MAIN_COLOR,
            timestamp=datetime.now(),
            description='PDC Utilities is an open-source bot using the MIT Licence and is actively developed by Pinkhron'
        ).add_field(
            name='Versioning:',
            value=f'- [**Python**](https://python.org) | v{platform.python_version()}\n'
                  f'- [**PDC Utilities**](https://github.com/Pinkhron/PDC-Utilities) | v{Data.VERSION}\n'
                  f'- [**Discord.py**](https://github.com/Rapptz/discord.py) | v{discord.__version__}'
        ).set_footer(text=Data.NAME, icon_url=Data.ICON))

    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(Data.TXT_NEWCOMERS)
    guild = bot.get_guild(Data.GUILD_ID)
    memberrole = guild.get_role(Data.ROLE_MEMBER)
    memberobject = guild.get_member(member.id)
    remaining = 3600

    await channel.set_permissions(memberrole, send_messages=True)
    await channel.set_permissions(memberobject, send_messages=True)
    message = await channel.send(embed=discord.Embed(
        title=f'{Data.EMOTE_MEMBER} A new member has joined PDC!',
        color=Data.MAIN_COLOR,
        description=f'<@!{member.id}> has joined PDC. This channel will be opened for an hour until a button is pressed'
                    f'. Please refer to pins to make sure your taking correct actions.',
    ).set_footer(text=Data.NAME, icon_url=Data.ICON))
    await message.pin()

    while remaining > 0:
        time.sleep(1)
        remaining -= 1

    if remaining < 0:
        await channel.set_permissions(memberrole, send_messages=False)
        await channel.set_permissions(memberobject, send_messages=False)
        await channel.send(embed=discord.Embed(
            title=f':lock: <#{Data.TXT_NEWCOMERS}> has been locked',
            color=Data.MAIN_COLOR,
            description=f'Channel has been locked due to `{"a button being pressed" if time == 0 else "button timeout"}`. '
                        f'Channel will be unlocked once a new member joins.'
        ).set_footer(text=Data.NAME, icon_url=Data.ICON))
        await message.unpin()


# $Commands
@bot.command()
@commands.is_owner()
async def sync(ctx):
    try:
        await ctx.send('Syncing (/) command to guild..')
        await bot.tree.sync(guild=discord.Object(id=Data.GUILD_ID))
        await ctx.send('Successfully synced (/) commands to guild')
    except discord.errors.Forbidden:
        await ctx.send('Error syncing (/) commands')

bot.run(TOKEN)
