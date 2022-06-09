from discord import app_commands
from discord.ext import commands
import discord

from data import Data

# Embeds

_confirmation = discord.Embed(title='Are you sure?',
                              description='Are you sure you want to start a new says game? This confirmation is here to'
                                          ' make sure this wasn\'t a mistake. **Starting a game for no reason will get '
                                          'you blacklisted from using Says as host for a week!**',
                              color=0x00FF00)
_confirmation.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(emoji='✅', label='Confirm', style=discord.ButtonStyle.green)
    async def _accept(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=discord.Embed(description=f'{Data.EMOTE_LOAD} '
                                                                                'Preparing for a new game..'))
        self.value = True
        self.stop()

    @discord.ui.button(emoji='❌', label='Cancel', style=discord.ButtonStyle.red)
    async def _deny(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=discord.Embed(description=f'{Data.EMOTE_LOAD} Cancelling..'),
                                                ephemeral=True)
        self.value = False
        self.stop()


class Says(commands.GroupCog, name='says'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    # Slash commands

    @app_commands.command(name='start', description='Starts a new game of Says')
    @app_commands.checks.has_role(Data.ROLE_MEMBER)
    async def _start(self, interaction: discord.Interaction):
        view = Confirm()
        await interaction.response.send_message(embed=_confirmation, view=view, ephemeral=True)
        await view.wait()

        if view.value is None:
            await interaction.edit_original_message(content=':clock3: Timed out')
        elif view.value:
            await interaction.edit_original_message(content=':eyes: coming soon')
        else:
            await interaction.edit_original_message(content=':x: Cancelled')


async def setup(bot: commands.Bot):
    await bot.add_cog(Says(bot), guild=discord.Object(id=Data.GUILD_ID))
