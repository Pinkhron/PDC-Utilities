import os
import random
import platform
from datetime import datetime

import discord
from discord.ext import commands
from discord.utils import get

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
        await message.reply(content=f'is {random.choice(["epic", "awesome", "amazing", "the best", "on fire :fire:"])}')

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
    # Button
    class Confirmation(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None

        @discord.ui.button(emoji='✅', label='Confirm', style=discord.ButtonStyle.green)
        async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message(content=f'<@!{interaction.user.id}> Confirming..')
            self.value = 1
            self.stop()

        @discord.ui.button(emoji='❌', label='Deny', style=discord.ButtonStyle.gray)
        async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message(content=f'<@!{interaction.user.id}> Kicking user..')
            self.value = 0
            self.stop()

        @discord.ui.button(emoji='🕒', label='Void', style=discord.ButtonStyle.red)
        async def void(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message(content=f'<@!{interaction.user.id}> Removing kick timer..')
            self.value = 2
            self.stop()

    # Response
    general = bot.get_channel(Data.TXT_GENERAL)
    view = Confirmation()

    message = await general.send(embed=discord.Embed(
        title=f'{Data.EMOTE_MEMBER} A new member has joined PDC!',
        color=0x1F8B4C,
        timestamp=datetime.now(),
        description='placeholder'
    ).set_footer(text=Data.NAME, icon_url=Data.ICON), view=view)

    await view.wait()
    if view.value is None:
        await member.kick(reason='Failed to be confirmed upon join')
        await message.edit(content=f'<@!{member.id}> has been auto-kicked due to button timeout', suppress=True)
    elif view.value == 1:
        await member.add_roles(get(member.guild.roles, id=Data.ROLE_MEMBER))
        await general.send(content=f'Successfully granted <@!{member.id}> access into the server')
    elif view.value == 0:
        await member.kick(reason='Kicked by a PDC member upon join')
        await general.send(content=f'Successfully kicked new member <@!{member.id}> upon user request')
    elif view.value == 2:
        await general.send(content=f'Successfully voided <@!{member.id}>\'s auto-kick timer')


@bot.command()
@commands.is_owner()
async def sync (ctx):
    try:
        await ctx.send('Syncing (/) command to guild..')
        await bot.tree.sync(guild=discord.Object(id=Data.GUILD_ID))
        await ctx.send('Successfully synced (/) commands to guild')
    except discord.errors.Forbidden:
        await ctx.send('Error syncing (/) commands')

bot.run(TOKEN)
