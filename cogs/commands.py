import logging

import discord
from discord import app_commands
from discord.ext import commands

from utils.storage_manager import StorageManager

log = logging.getLogger(__name__)

class Commands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot=bot
        self.storage=StorageManager(
            history_path=".history.json",
            daily_image_path=".daily_image.json",
            max_history_size=20
        )
    
    @app_commands.command(name="DailyImage", description="Send Daily Image")
    async def send_daily_image(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        try:
            image_path = self.storage.get_daily_image()
            if image_path:
                await interaction.followup.send(file=discord.File(image_path))
            else:
                await interaction.followup.send("Failed to find image.", ephemeral=True)
        except Exception as e:
            log.error("Failed to send daily image.", exc_info=e)
            if not interaction.response.is_done():
                await interaction.response.send_message("Error occured.", ephemeral=True)

async def setup(bot: commands.Bot, storage) -> None:
    await bot.add_cog(Commands(bot), storage)