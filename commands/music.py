from discord import app_commands
from discord.ext import commands
import discord

from data import Data

# Embeds

_noGlobalEmbed = discord.Embed(description=':x: You must be in "Global VC" to run this command', color=0xFF0000)
_notInVc = discord.Embed(description=':x: I am not in a voice channel')

_connectedEmbed = discord.Embed(description='<a:PDC_Success:981093316114399252> Connected!', color=0x198754)
_disconnectedEmbed = discord.Embed(description='<a:PDC_Success:981093316114399252> Successfully disconnected!',
                                   color=0xFF0000)


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='join')  # Join VC
    @app_commands.guilds(discord.Object(id=Data.GUILD_ID))
    @app_commands.checks.cooldown(1, 60.0, key=lambda i: i.user.id)
    async def _join(self, interaction: discord.Interaction) -> None:
        if not interaction.user.voice.channel == Data.VC_GLOBAL:
            await interaction.response.send_message(embed=_noGlobalEmbed)
            return
        else:
            vc = interaction.user.voice.channel
            await interaction.response.send_message(embed=_connectedEmbed)
        await vc.connect()

    @app_commands.command(name='disconnect')  # Disconnect from VC
    @app_commands.guilds(discord.Object(id=Data.GUILD_ID))
    @app_commands.checks.cooldown(1, 60.0, key=lambda i: i.user.id)
    async def _disconnect(self, interaction: discord.Interaction):
        if not interaction.user.voice.channel == Data.VC_GLOBAL:
            await interaction.response.send_message(embed=_noGlobalEmbed)
        else:
            vc = interaction.message.guild.voice_client

            if not vc:
                await interaction.response.send_message(embed=_notInVc)
            else:
                await vc.disconnect()
                await interaction.response.send_message(embed=_disconnectedEmbed)

    # Error handling

    @_join.error
    @_disconnect.error
    async def join_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):  # Cooldown
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(str(error), ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Music(bot))
