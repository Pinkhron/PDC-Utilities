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

_new = discord.Embed(title='Welcome to Says!', description='The host will be in full control of the game with host '
                                                           'slash commands. To invite players to the game use '
                                                           '`/says invite <usr>`, it will send a confirmation DM to '
                                                           'the user to whom you (host) invited. To read more on how '
                                                           'to play please check the pins or '
                                                           f'[click here]({_readme}).')
_new.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(emoji='✅', label='Confirm', style=discord.ButtonStyle.green)
    async def _accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content=f'<@!{interaction.user.id}>',
                                                embed=discord.Embed(description=f'{Data.EMOTE_LOAD} Starting a new game'
                                                                                '..'))
        self.value = True
        self.stop()

    @discord.ui.button(emoji='❌', label='Cancel', style=discord.ButtonStyle.grey)
    async def _deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content=f'Cancelled', ephemeral=True)
        self.value = False
        self.stop()


class Says(commands.GroupCog, name='says'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    # Slash commands (CHANGE ROLE ON RELEASE)

    @app_commands.command(name='start', description='Starts a new game of Says')
    @app_commands.checks.cooldown(1, 30, key=lambda i: i.user.id)
    @app_commands.checks.has_role(Data.ROLE_ORGANIZER)
    async def _start(self, interaction: discord.Interaction):
        view = Confirm()
        await interaction.response.send_message(embed=_confirmation, view=view, ephemeral=True)
        await view.wait()

        if view.value is None:
            await interaction.response.send_message(content=':clock3: Timed out', ephemeral=True)
        elif view.value:
            await interaction.response.send_message(content=':eyes: coming soon')

            host = get(interaction.guild.roles, name="SAYS HOST")  # Give host role
            await interaction.user.add_roles(host)

            channel = self.bot.get_channel(Data.TXT_SAYS)
            await channel.send(content=f'**:game_die: A new game of Says has begun!** Host: <@!{interaction.user.id}>',
                               embed=_new)
        else:
            return

    # Error handling

    @_start.error
    async def err(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):  # Command cooldown
            await interaction.response.send_message(str(error), ephemeral=True)
        elif isinstance(error, app_commands.MissingPermissions):  # Missing perms
            await interaction.response.send_message(str(error), ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Says(bot), guild=discord.Object(id=Data.GUILD_ID))
