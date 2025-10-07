import datetime
import os
import logging
from zoneinfo import ZoneInfo

import discord
from discord import app_commands
from discord.ext import commands

from utils.daily_image import daily_image
from utils.storage_manager import storage_manager

log = logging.getLogger(__name__)

TIMEZONE = ZoneInfo(os.getenv("TIMEZONE", "Asia/Seoul"))

class Commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot
        self.storage_path="./storage"
    
    @app_commands.command(name="dailyimage", description="Send Daily Image")
    async def send_daily_image(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        try:
            image_path: str | None = storage_manager.get_daily_image()
            if image_path is None:
                today_str = datetime.datetime.now(TIMEZONE).strftime("%Y-%m-%d")
                image_path = daily_image.select_daily_image(today_str)

            if image_path:
                await interaction.followup.send(file=discord.File(os.path.join(self.storage_path, image_path)))
            else:
                await interaction.followup.send("Failed to find image.", ephemeral=True)
        except Exception as e:
            log.error("Failed to send daily image.", exc_info=e)
            if not interaction.response.is_done():
                await interaction.response.send_message("Error occured.", ephemeral=True)
    
    @app_commands.command(name="reselect_dailyimage", description="Reselect Daily Image")
    async def reselect_daily_image(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        try:
            today_str = datetime.datetime.now(TIMEZONE).strftime("%Y-%m-%d")
            image_path = daily_image.select_daily_image(today_str)

            if image_path:
                await interaction.followup.send(file=discord.File(image_path))
            else:
                await interaction.followup.send("Failed to find image.", ephemeral=True)
        except Exception as e:
            log.error("Failed to reselect daily image.", exc_info=e)
            if not interaction.response.is_done():
                await interaction.response.send_message("Error occured.", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Commands(bot))