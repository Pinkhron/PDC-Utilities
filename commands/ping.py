import discord

from main import bot, Data  # Discord.py stuff & JSON Data

# Embed

_pingEmbed = discord.Embed(title=':ping_pong: Pong!', description=f'```{round(bot.latency * 1000)}ms```')
_pingEmbed.set_footer(text=Data.FOOTER, icon_url=Data.LOGO_BOT)


# Slash Command

@bot.tree.command(guild=discord.Object(id=Data.GUILD_ID), name='ping',
                  description='Tests the ping between Discord and PDC Utilities')
async def _ping(interaction: discord.Interaction):
    await interaction.response.send_message(embed=_pingEmbed)


# Discord.py setup

def setup():
    bot.tree.add_command(_ping)
