import discord
from discord import app_commands
from discord.ext import commands

from crontab import CronTab
from data import Data

# File config
cron = CronTab(user='pin')


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = False

    @discord.ui.button(emoji='✅', label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content='Message pinned successfully')
        self.value = True
        self.stop()

    @discord.ui.button(emoji='❌', label='Cancel', style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(content='Cancelled')
        self.value = False
        self.stop()


class Pin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description='Temporary pin a message for 24hrs')
    @app_commands.checks.cooldown(1, 300.0, key=lambda i: i.user.id)
    async def pin(self, interaction=discord.Interaction, messageid=int):
        # Variables
        channel = await self.bot.fetch_channel(interaction.channel_id)
        message = await channel.fetch_message(int(messageid))

        if not interaction.channel_id == Data.TXT_GENERAL:
            await interaction.response.send_message(
                content=f'Temporary pinning is only supported in <#{Data.TXT_GENERAL}>',
            )
            return
        elif message.pinned:
            await interaction.response.send_message(
                content=f':x: Message is already pinned!',
            )
            return

        view = Confirm()

        interaction.response.send_message(embed=discord.Embed(
            title='Are you sure?',
            color=Data.MAIN_COLOR,
            description=f'Are you sure you want to pin the message by <@!{message.author.id}> with content '
                        f'"{message.content}"?\n\n'
                        f'**Message will be only pinned for 24hrs**'
        ).set_footer(text=Data.NAME, icon_url=Data.ICON), view=view)

        await view.wait()
        if view.value is True:
            await message.pin()
            job = cron.new(command=f'python3 ../scripts/unpin.py {messageid}', comment=f'{messageid}')
            job.day.every(1)
        elif view.value is None:
            return
        else:
            return

    # Error handling
    @pin.error
    async def error(self, interaction=discord.Interaction, error=app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(str(error), ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Pin(bot))
