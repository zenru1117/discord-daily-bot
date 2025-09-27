from collections import deque
import datetime
import logging
import os
import random
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands, tasks

from utils.storage_manager import DailyImage, StorageManager

log = logging.getLogger(__name__)

TARGET_CHANNEL_ID = os.getenv("TARGET_CHANNEL_ID")
MAX_HISTORY_SIZE = int(os.getenv("MAX_HISTORY_SIZE", 20))
TIMEZONE = ZoneInfo(os.getenv("TIMEZONE", "Asia/Seoul"))
SCHEDULED_TIME = datetime.time(hour=23, minute=12, second=0, tzinfo=TIMEZONE)

class Sender(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot
        self.storage_dir="./storage"

        self.storage = StorageManager(
            history_path=".history.json",
            daily_image_path=".daily_image.json",
            max_history_size=MAX_HISTORY_SIZE
        )

        if TARGET_CHANNEL_ID:
            self.channel_id = int(TARGET_CHANNEL_ID)
            self.scheduled_image_sender.start()
            log.info("Starting schedule.")
        else:
            log.warning("TARGET_CHANNEL_ID is not defined.")
    
    def cog_unload(self):
        if self.scheduled_image_sender.is_running():
            self.scheduled_image_sender.cancel()

    def _select_daily_image(self, today_str: str) -> str | None:
        log.info(f"Select new daily image for {today_str}")

        if not os.path.isdir(self.storage_dir): return None
        images = [f for f in os.listdir(self.storage_dir) if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]
        if not images: return

        select_history: deque[str] = self.storage.get_history()
        candidate_images = [img for img in images if img not in select_history]
        if not candidate_images:
            log.info("All images were recently used. Ignoring history and reselecting.")
            candidate_images = images
        
        chosen_image = random.choice(candidate_images)

        select_history.append(chosen_image)
        self.storage.save_history(select_history)

        daily_image: DailyImage = {"date": today_str, "name": chosen_image}
        self.storage.save_daily_image(daily_image)

        log.info(f"New daily image selected '{chosen_image}'.")
        return os.path.join(self.storage_dir, chosen_image)
    
    @tasks.loop(time=SCHEDULED_TIME)
    async def scheduled_image_sender(self) -> None:
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(self.channel_id)
    
        if not (channel and isinstance(channel, discord.TextChannel)):
            log.error(f"Schedule channel ID ({self.channel_id}) not found or is not a text channel.")
            return
        
        today_str = datetime.datetime.now(TIMEZONE).strftime("%Y-%m-%d")
        image_path = self._select_daily_image(today_str)
        if image_path:
            await channel.send(file=discord.File(image_path))
            log.info(f"Sent the scheduled image to channel '{channel.name}'.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Sender(bot))