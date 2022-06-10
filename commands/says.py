import asyncio
import datetime

from discord import app_commands
from discord.ext import commands
from discord.utils import get
import discord

from data import Data

# Embeds

_readme = 'https://discord.com/channels/966934902878646323/984309064244817931/984365351460548648'

_confirmation = discord.Embed(title='Are you sure?',
                              description='Are you sure you want to start a new says game? This confirmation is here to'
                                          ' make sure this wasn\'t a mistake. **Starting a game for no reason will get '
                                          'you blacklisted from using Says as host for a week!**',
                              color=0x00FF00)
_confirmation.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)

_new = discord.Embed(title=':video_game: Welcome to PDC\'s Says!',
                     description='The host will be in full control of the game '
                                 'with host slash commands. To invite players to the game use'
                                 ' `/says invite <usr>`, it will send a confirmation DM to '
                                 'the user to whom you (host) invited. To read more on how '
                                 'to play please check the pins or '
                                 f'[click here]({_readme}).',
                     color=0x00FF00)
_new.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)


class Confirm(discord.ui.View):  # Confirm game start
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(emoji='✅', label='Confirm', style=discord.ButtonStyle.green)
    async def _confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content=f'<@!{interaction.user.id}>',
                                                embed=discord.Embed(description=f'{Data.EMOTE_LOAD} Starting a new game'
                                                                                '..'))
        self.value = True
        self.stop()

    @discord.ui.button(emoji='❌', label='Cancel', style=discord.ButtonStyle.grey)
    async def _cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content=f'Cancelled', ephemeral=True)
        self.value = False
        self.stop()


class Invite(discord.ui.View):  # Accept/decline invite
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(emoji='✅', label='Accept', style=discord.ButtonStyle.green)
    async def _accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=discord.Embed(description=':grin: Successfully accepted invite!'))
        self.value = True
        self.stop()

    @discord.ui.button(emoji='❌', label='Decline', style=discord.ButtonStyle.grey)
    async def _decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=discord.Embed(description=':x: Successfully declined invite'))
        self.value = False
        self.stop()


class Says(commands.GroupCog, name='says'):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

        # Game variables

        self.running = False  # False: Ready | True: Game running | None: Dormant
        self.time = 0

        self.host = 0
        self.cohost = []
        self.participants = []
        self.invitees = []
        self.eliminated = []

    # Host & co-host commands

    @app_commands.command(name='start', description='Starts a new game of Says')
    @app_commands.checks.cooldown(1, 5, key=lambda i: i.user.id)
    @app_commands.checks.has_role(Data.ROLE_ORGANIZER)
    async def _start(self, interaction: discord.Interaction):
        _dormant = discord.Embed(title=':zzz: This channel has been marked as dormant.',
                                 description='This channel is now marked as dormant due to an inactive Says game or a  '
                                             'game the recently ended. You will not be able to launch another game of '
                                             'Says for the next `5 minutes`. In the meantime, you can read how to play '
                                             f'Says [**here**]({_readme}).')
        _dormant.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)

        _ready = discord.Embed(title=f':white_check_mark: <#{Data.TXT_SAYS}> is now ready!',
                               description=f'<#{Data.TXT_SAYS}> is now available to be played! Run `/says start` to '
                                           f'start a game as a host. [Click here]({_readme}) for more info on Says.')
        _ready.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)

        if self.running == (True or None):
            await interaction.response.send_message(content='Sorry, but a game is already running. '
                                                            'Please try again later.', ephemeral=True)

        view = Confirm()
        await interaction.response.send_message(embed=_confirmation, view=view, ephemeral=True)
        await view.wait()

        if view.value is None:  # Timeout
            await interaction.response.send_message(content=':clock3: Timed out', ephemeral=True)
        elif view.value:  # Start game
            host = get(interaction.guild.roles, id=Data.ROLE_SAYS_HOST)  # Give host role
            await interaction.user.add_roles(host)

            self.running = True  # Set game to running
            self.time = 3600
            self.host = interaction.user.id  # Set host

            channel = self.bot.get_channel(Data.TXT_SAYS)
            await channel.send(content=f'**:game_die: A new game of PDC Says has begun!** Host: '
                                       f'<@!{interaction.user.id}>',
                               embed=_new)

            while self.time > 0:
                self.timer = datetime.timedelta(seconds=self.time)
                await asyncio.sleep(1)
                self.time -= 1
            await self.bot.get_channel(Data.TXT_SAYS).send(embed=_dormant)
            self.running = None
            await asyncio.sleep(300)
            await self.bot.get_channel(Data.TXT_SAYS).send(embed=_ready)
        else:  # Cancelled
            return

    @app_commands.command(name='end', description='HOST: Ends game')
    @app_commands.checks.cooldown(1, 10, key=lambda i: i.user.id)
    @app_commands.checks.has_role(Data.ROLE_SAYS_HOST)
    async def _end(self, interaction: discord.Interaction):
        if interaction.user.id == self.host:
            self.time = 0
            await interaction.response.send_message(content='Ended game successfully!')

    @app_commands.command(name='invite', description='HOST: Invites a user into the game')
    @app_commands.checks.cooldown(1, 2, key=lambda i: i.user.id)
    @app_commands.checks.has_role(Data.ROLE_SAYS_HOST)
    async def _invite(self, interaction: discord.Interaction, usr1: discord.Member):
        _invite = discord.Embed(title=':video_game: You have been invited to a game of PDC Says',
                                description=f'<@!{interaction.user.id}> is hosting a game of PDC Says and has '
                                            f'invited you to play! You can accept/decline the invite with the buttons '
                                            f'below.',
                                color=0xCC8899)  # Invite embed
        _invite.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)

        _timeout = discord.Embed(title=':clock3: Invite timed out!', description=f'<@!{usr1.id}>\'s invite has been '
                                                                                 f'invalidated due to a response not '
                                                                                 f'being sent. If this was a mistake, '
                                                                                 f'invite them again.',
                                 color=0x808080)
        _timeout.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)

        _accepted = discord.Embed(title=':grin: Invite accepted!', description=f'<@!{usr1.id}> Has accepted your game '
                                                                               f'invite! They will be added into the '
                                                                               f'game shortly!')
        _accepted.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)

        _declined = discord.Embed(title=f':x: User declined invite', description=f'<@!{usr1.id}> has declined your '
                                                                                 f'invite. Please don\'t invite them '
                                                                                 f'again unless this was a mistake!')
        _declined.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)

        if usr1.id in (self.invitees or self.participants):
            await interaction.response.send_message(content=':x: Failed to invite user. This error shows when the '
                                                            'user has already accepted your invite or one had '
                                                            'already been sent out.')
            return
        elif usr1.id in self.host:
            await interaction.response.send_message(content=':x: You cannot invite a host! :clown:')
            return

        view = Invite()

        dm = await usr1.create_dm()
        channel = self.bot.get_channel(Data.TXT_SAYS)

        await dm.send(embed=_invite, view=view)
        await interaction.response.send_message(content=f'<@!{interaction.user.id}>',
                                                embed=discord.Embed(description='<a:PDC_Success:981093316114399252> '
                                                                                f'Successfully invited <@!{usr1.id}>!'))
        await view.wait()
        self.invitees.append(usr1.id)

        if view.value is None:
            await dm.send(':clock3: Timed out')
            await channel.send(content=f'<@!{interaction.user.id}>', embed=_timeout)
            self.invitees.remove(usr1.id)
        elif view.value:
            await channel.send(content=f'<@!{interaction.user.id}>', embed=_accepted)
            self.invitees.remove(usr1.id)
            self.participants.append(usr1.id)

            participant = get(interaction.guild.roles, id=Data.ROLE_SAYS_PARTICIPANT)
            await usr1.add_roles(participant)
        else:
            await channel.send(content=f'<@!{interaction.user.id}>', embed=_declined)
            self.invitees.remove(usr1.id)
            return

    # @everyone commands

    @app_commands.command(name='time', description='EVERYONE: Shows the amount of time left on your game')
    @app_commands.checks.cooldown(1, 2, key=lambda i: i.user.id)
    async def _time(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=discord.Embed(title=':clock3: Time remaining..',
                                                                    description=self.timer))

    # Error handling

    @_invite.error
    @_start.error
    async def err(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):  # Command cooldown
            await interaction.response.send_message(str(error), ephemeral=True)
        elif isinstance(error, app_commands.MissingPermissions):  # Missing perms
            await interaction.response.send_message(str(error), ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Says(bot), guild=discord.Object(id=Data.GUILD_ID))
