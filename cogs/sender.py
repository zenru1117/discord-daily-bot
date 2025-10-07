import datetime
import logging
import os
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands, tasks

from utils.daily_image import daily_image

log = logging.getLogger(__name__)

TARGET_CHANNEL_ID = os.getenv("TARGET_CHANNEL_ID")
MAX_HISTORY_SIZE = int(os.getenv("MAX_HISTORY_SIZE", 20))
TIMEZONE = ZoneInfo(os.getenv("TIMEZONE", "Asia/Seoul"))
SCHEDULED_TIME = datetime.time(hour=23, minute=12, second=0, tzinfo=TIMEZONE)

class Sender(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot

        if TARGET_CHANNEL_ID:
            self.channel_id = int(TARGET_CHANNEL_ID)
            self.scheduled_image_sender.start()
            log.info("Starting schedule.")
        else:
            log.warning("TARGET_CHANNEL_ID is not defined.")
    
    async def cog_unload(self) -> None:
        if self.scheduled_image_sender.is_running():
            self.scheduled_image_sender.cancel()
    
    @tasks.loop(time=SCHEDULED_TIME)
    async def scheduled_image_sender(self) -> None:
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(self.channel_id)
    
        if not (channel and isinstance(channel, discord.TextChannel)):
            log.error(f"Schedule channel ID ({self.channel_id}) not found or is not a text channel.")
            return
        
        today_str = datetime.datetime.now(TIMEZONE).strftime("%Y-%m-%d")
        image_path = daily_image.select_daily_image(today_str)
        if image_path:
            await channel.send(file=discord.File(image_path))
            log.info(f"Sent the scheduled image to channel '{channel.name}'.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Sender(bot))