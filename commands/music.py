import os

from discord.utils import get
from discord import app_commands
from discord.ext import commands
import discord

import youtube_dl
from data import Data

# Embeds

_noVcEmbed = discord.Embed(description=':x: You must be a VC run this command', color=0xFF0000)
_notInVc = discord.Embed(description=':x: I am not in a voice channel')

_connectedEmbed = discord.Embed(description='<a:PDC_Success:981093316114399252> Connected!', color=0x198754)
_disconnectedEmbed = discord.Embed(description='<a:PDC_Success:981093316114399252> Successfully disconnected!',
                                   color=0xFF0000)


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='join', description='Joins VC')  # Join VC
    @app_commands.guilds(discord.Object(id=Data.GUILD_ID))
    async def _join(self, interaction: discord.Interaction) -> None:
        if not interaction.user.voice:
            await interaction.response.send_message(embed=_noVcEmbed)
            return
        else:
            vc = interaction.user.voice.channel
            await interaction.response.send_message(embed=_connectedEmbed)
        await vc.connect()

    @app_commands.command(name='disconnect', description='Force disconnect from VC')  # Disconnect from VC
    @app_commands.guilds(discord.Object(id=Data.GUILD_ID))
    async def _disconnect(self, interaction: discord.Interaction) -> None:
        voice_client = interaction.guild.voice_client

        if not voice_client:
            await interaction.response.send_message(embed=_notInVc)
            return
        else:
            await interaction.response.send_message(embed=_disconnectedEmbed)
        return await voice_client.disconnect(force=True)

    @app_commands.command(name='play', description='Plays a song in a VC')
    @app_commands.guilds(discord.Object(id=Data.GUILD_ID))
    async def _play(self, interaction: discord.Interaction, url: str):
        voice_client = interaction.guild.voice_client
        voice = get(self.bot.voice_clients, guild=interaction.guild)
        vc = interaction.user.voice.channel

        if not voice_client:
            if not interaction.user.voice:
                await interaction.response.send_message(embed=_noVcEmbed)
                return
            else:
                await vc.connect()

        if url.startswith('https://www.youtube.com/watch?v='):  # YouTube Player
            song = os.path.isfile('song.mp3')
            try:
                if song:
                    os.remove('song.mp3')
            except PermissionError:
                await interaction.response.send_message(content='Please wait for the song to finish playing')
                return

            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            for file in os.listdir('./'):
                if file.endswith('.mp3'):
                    os.rename(file, 'song.mp3')

            voice.play(discord.FFmpegAudio('song.mp3'))
            voice.volume = 100
            voice.is_playing()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Music(bot))
