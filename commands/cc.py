import discord
from discord import app_commands
from discord.ext import commands

from data import Data


class CCCreateConfirmation(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(emoji='✅', label='Confirm', style=discord.ButtonStyle.green)
    async def _confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content='Creating Channel..')
        self.value = True
        self.stop()

    @discord.ui.button(emoji='❌', label='Cancel', style=discord.ButtonStyle.gray)
    async def _cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content='Cancelled')
        self.value = False
        self.stop()

    @discord.ui.button(emoji='📜', label='CC Help & Guidelines', style=discord.ButtonStyle.blurple)
    async def _help(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            embed=discord.Embed(
                title=':scroll: CC Help & Guidelines',
                color=Data.CLR_BLURPLE,
                description='**Help:**\n\n'
                            'You will have a private channel (like a private thread). You will have '
                            '"Manage Channel", "Manage Permissions" (Bot Controlled), "@everyone & @here" & '
                            '"Manage Webhooks" IN YOUR CHANNEL unless the creator of the channel grants you permissions.\n\n'
                            '**CC Rules:**\n\n'
                            ' - If you channel happens to be NSFW, please toggle NSFW\n'
                            ' - Don\'t create a CC if you just have the intention to mass ping people\n'
                            ' - Don\'t abuse your powers\n'
                            ' - I am required (by discord) to check channels every one in a while. If you want to get \n'
                            'past this create a private thread in the CC or general.\n'
                            ' - Have fun!'
            ).set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)
        )
        self.value = False
        self.stop()


class CustomChannel(commands.GroupCog, name='cc'):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @app_commands.command(name='create', description='Custom Channel: Creates a custom channel')
    @app_commands.guilds(discord.Object(id=Data.GUILD_ID))
    async def create(self, interaction: discord.Interaction):
        # Checks

        if not interaction.channel_id == Data.TXT_BOTS:
            await interaction.response.send_message(
                content=f':x: You cannot use this (/) command here. Go to <#{Data.TXT_BOTS}>',
                ephemeral=True
            )
            return

        # Command

        view = CCCreateConfirmation()

        await interaction.response.send_message(
            content=f'<@!{interaction.user.id}>',
            view=view,
            embed=discord.Embed(
                title='Welcome to PDC\'s CC Creation System',
                color=Data.CLR_PDC,
                description='Here you can create a custom channel that you will be able to manage on your own. This '
                            'includes adding members, @everyone perms, and more (in channel). **DISCLAIMER:** If you '
                            'don\'t follow the CC channel guidelines (click button below) your channel will be deleted '
                            'and you will be blacklisted for a week from CC creation.'
            ).set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)
        )
        await view.wait()

        if view.value is None:
            await interaction.response.send_message(
                content=':clock3: Timed out. Please run the command again if you wish to proceed',
                ephemeral=True
            )
        elif view.value:
            pass
        else:
            return


async def setup(bot: commands.Bot):
    await bot.add_cog(CustomChannel(bot), guild=discord.Object(id=Data.GUILD_ID))
