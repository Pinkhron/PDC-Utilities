import asyncio

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

_new = discord.Embed(title=':video_game: Welcome to Says!',
                     description='The host will be in full control of the game '
                                 'with host slash commands. To invite players to the game use'
                                 ' `/says invite <usr>`, it will send a confirmation DM to '
                                 'the user to whom you (host) invited. To read more on how '
                                 'to play please check the pins or '
                                 f'[click here]({_readme}).',
                     color=0x00FF00)
_new.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)

_sleep = discord.Embed()


class Confirm(discord.ui.View):  # Confirm game start
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(emoji='✅', label='Confirm', style=discord.ButtonStyle.green)
    async def _confirm(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f'<@!{interaction.user.id}>',
                                                embed=discord.Embed(description=f'{Data.EMOTE_LOAD} Starting a new game'
                                                                                '..'))
        self.value = True
        self.stop()

    @discord.ui.button(emoji='❌', label='Cancel', style=discord.ButtonStyle.grey)
    async def _cancel(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f'Cancelled', ephemeral=True)
        self.value = False
        self.stop()


class Invite(discord.ui.View):  # Accept/decline invite
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(emoji='✅', label='Accept', style=discord.ButtonStyle.green)
    async def _accept(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=discord.Embed(description=':grin: Successfully accepted invite!'))
        self.value = True
        self.stop()

    @discord.ui.button(emoji='❌', label='Decline', style=discord.ButtonStyle.grey)
    async def _decline(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=discord.Embed(description=':x: Successfully declined invite'))
        self.value = False
        self.stop()


class Says(commands.GroupCog, name='says'):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

        # Game variables

        self.running = False
        self.host = 0
        self.participants = []
        self.invitees = []
        self.eliminated = []

    # Slash commands (CHANGE ROLE ON RELEASE)

    @app_commands.command(name='start', description='Starts a new game of Says')
    @app_commands.checks.cooldown(1, 30, key=lambda i: i.user.id)
    @app_commands.checks.has_role(Data.ROLE_ORGANIZER)
    async def _start(self, interaction: discord.Interaction):
        if self.running:
            await interaction.response.send_message(content='Sorry, but a game is already running. '
                                                            'Please try again later.', ephemeral=True)

        view = Confirm()
        await interaction.response.send_message(embed=_confirmation, view=view, ephemeral=True)
        await view.wait()

        if view.value is None:  # Timeout
            await interaction.response.send_message(content=':clock3: Timed out', ephemeral=True)
        elif view.value:  # Start game
            host = get(interaction.guild.roles, name="SAYS HOST")  # Give host role
            await interaction.user.add_roles(host)

            self.running = True  # Set game to running
            self.host = interaction.user.id  # Set host

            channel = self.bot.get_channel(Data.TXT_SAYS)
            await channel.send(content=f'**:game_die: A new game of PDC Says has begun!** Host: '
                                       f'<@!{interaction.user.id}>',
                               embed=_new)
        else:  # Cancelled
            return

    @app_commands.command(name='invite', description='HOST: Invites a user into the game')
    @app_commands.checks.cooldown(1, 2, key=lambda i: i.user.id)
    @app_commands.checks.has_role(Data.ROLE_SAYS_HOST)
    async def _invite(self, interaction: discord.Interaction, usr1: discord.User):
        _invite = discord.Embed(title='You have been invited to a game of PDC Says',
                                description=f'<@!{self.host}> is hosting a game of PDC Says and has '
                                            f'invited you to play! You can accept/decline the invite with the buttons '
                                            f'below.')  # Invite embed
        _invite.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)

        _timeout = discord.Embed(title=':clock3: Invite timed out!', description=f'<@!{usr1.id}>\'s invite has been '
                                                                                 f'invalidated due to a response not '
                                                                                 f'being sent. If this was a mistake, '
                                                                                 f'invite them again.')
        _timeout.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)

        _accepted = discord.Embed(title=':grin: Invite accepted!', description=f'<@!{usr1.id}> Has accepted your game '
                                                                               f'invite! They will be added into the '
                                                                               f'game shortly!')
        _accepted.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)

        _declined = discord.Embed(title=f':x: User declined invite', description=f'<@!{usr1.id}> has declined your '
                                                                                 f'invite. Please don\'t invite them '
                                                                                 f'again unless this was a mistake!')
        _declined.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)

        for i in self.invitees:
            if i == self.invitees[i]:
                await interaction.response.send_message(content=':x: Failed to invite user. This error shows when the '
                                                                'user has already accepted your invite or one had '
                                                                'already been sent out.')

        view = Invite()
        dm = await usr1.create_dm()
        await dm.send(embed=_invite, view=view)
        await view.wait()
        self.invitees.append(usr1.id)

        if view.value is None:
            await dm.send(':clock3: Timed out')
            await interaction.response.send_message(content=f'<@!{self.host}>', embed=_timeout)

            for i in self.invitees:
                if usr1.id == self.invitees[i]:
                    self.invitees.pop(i)
        elif view.value:
            await interaction.response.send_message(content=f'<@!{self.host}>', embed=_accepted)
            self.participants.append(usr1.id)
        else:
            await interaction.response.send_message(content=f'<@!{self.host}>', embed=_declined)

            for i in self.invitees:
                if usr1.id == self.invitees[i]:
                    self.invitees.pop(i)
            return

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
