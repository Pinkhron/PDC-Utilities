import os
import platform
from datetime import datetime

from discord.ext.commands import is_owner
from discord.ext import commands
from discord.utils import get
import discord

from dotenv import load_dotenv
from data import Data

# Load ENV

load_dotenv()
TOKEN = os.getenv('TOKEN')

# Initialize bot

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.guild_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='>', intents=intents, owner_id=597178180176052234)


class NewConfirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(emoji='❌', label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

    @discord.ui.button(emoji='✅', label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.stop()


@bot.event
async def on_ready():
    print('Successfully logged in as {0.user}'.format(bot))

    if __name__ == '__main__':  # File handling
        for cmd in os.listdir('./commands'):  # Slash commands
            if cmd.endswith('.py'):
                await bot.load_extension(f'commands.{cmd[:-3]}')


@bot.event
async def on_message(message):
    if message.author.bot:  # Doesn't respond to bots
        return

    if message.content.lower() == 'pdc':  # Respond to PDC
        await message.reply('is awesome', mention_author=False)

    if bot.user.mentioned_in(message) and len(bot.user.mention) == len(message.content):  # Mention embed
        version = Data.VERSION

        _mention = discord.Embed(title=f'\U0001F44B Hey, {message.author.name}!',
                                 description='PDC Utilities is an open-source bot made by <@597178180176052234> to '
                                             'make managing PDC easy & to make PDC fun! Click '
                                             '[**here**](https://discord.com/channels/966934902878646323/966958813565550592/984320243830755349) '
                                             f'or check pins in <#{Data.TXT_BOTS}> for a list of commands. '
                                             'PDC Utilities was made with Python & Discord.py\n\n'
                                             f'- [Python](https://python.org) | v{platform.python_version()}\n'
                                             f'- [Discord.py](https://github.com/Rapptz/discord.py) | v{discord.__version__}\n'
                                             f'- [PDC Utilities](https://github.com/Pinkhron/PDC-Utilities) | v{version}\n'
                                             f'[PinkhronNetwork Status](https://status.pinkhron.net)\n\n'
                                             'Thank you for joining PDC!')
        _mention.set_thumbnail(url=Data.LOGO_DEFAULT)
        _mention.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)

        await message.reply(embed=_mention)

    await bot.process_commands(message)


@bot.event
async def on_member_join(member):
    general = bot.get_channel(966934903381983324)
    view = NewConfirm()

    await general.send(embed=discord.Embed(
        title=':tickets: New Member',
        description=f'<@!{member.id}> has joined PDC. If you\'ve invited them please press accept. Accepting will grant '
                    f'them access to all of the member channels. If you invited someone by mistake/leaked invite press '
                    f'decline. Declining will kick them out of the server. **Inviting random people and granting them '
                    f'access into the server will get your account blacklisted from using this feature until further '
                    f'notice. All actions are logged.** You will have `3` minutes to respond before they are auto-kicked.',
        timestamp=datetime.now()
    ).set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT), view=view)
    await view.wait()

    if view.value is None:
        await member.kick()
        await general.send(content=f':clock3: Kicked <@!{member.id}> due to button timeout.')
    elif view.value is True:
        role = get(member.server.roles, name="MEMBER")
        await member.add_roles(role)
        await general.send(content=f':white_check_mark: Granted <@!{member.id}> access into the server.')
    else:
        await member.kick()
        await general.send(content=f'Kicked <@!{member.id}>')


# Regular commands

@bot.command(name='sync')  # Sync (/) commands
@is_owner()
async def _sync(ctx):
    await ctx.send('Syncing...')

    try:
        await bot.tree.sync(guild=discord.Object(id=Data.GUILD_ID))
        await ctx.send('Success!')
    except discord.errors.Forbidden:
        await ctx.send('Error')


@bot.command(name='ping')
async def _ping(ctx):
    _pingEmbed = discord.Embed(title=':ping_pong: Pong!', description=f'```{round(bot.latency * 1000)}ms```')
    _pingEmbed.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)

    await ctx.reply(embed=_pingEmbed, mention_author=False)

# Run bot


bot.run(TOKEN)
