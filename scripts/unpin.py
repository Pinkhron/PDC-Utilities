import sys

from discord.ext import commands

from crontab import CronTab
from data import Data

cron = CronTab(user='pin')


# Unpin message

class Unpin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        channel = await self.bot.fetch_channel(Data.TXT_GENERAL)
        message = await channel.fetch_message(int(sys.argv[1]))

        await message.unpin()

        job = cron.find_command(str(sys.argv[1]))
        cron.remove(job)


async def setup(bot: commands.Bot):
    await bot.add_cog(Unpin(bot))
