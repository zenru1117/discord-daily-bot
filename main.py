import os
import asyncio
from pathlib import Path

import uvloop
import discord
from discord.ext import commands
from dotenv import load_dotenv

from logger import setup_logging

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
TEST_GUILD_ID = os.getenv("TEST_GUILD_ID")

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

log = setup_logging("./logs", "botlog")

class DiscordDailyBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix="$",
            intents=intents,
            help_command=None
        )
    
    async def setup_hook(self) -> None:
        # load cogs
        for file_path in Path("./cogs").glob("*.py"):
            cog_name = file_path.stem
            try:
                await self.load_extension(f"cogs.{cog_name}")
                log.info(f"Loaded Cog: {cog_name}")
            except Exception as e:
                log.error(f"Failed to load Cog: {cog_name}", exc_info=e)
        
        # sync slash commands
        if TEST_GUILD_ID:
            guild = discord.Object(id=int(TEST_GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            log.info(f"Synced {len(synced)} commands to test guild {TEST_GUILD_ID}")
        else:
            synced = await self.tree.sync()
            log.info(f"Synced {len(synced)} global commands")
    
    async def on_ready(self) -> None:
        if self.user:
            log.info(f"Logged in {self.user.name} (ID: {self.user.id})")

def main() -> None:
    bot = DiscordDailyBot()
    bot.run(BOT_TOKEN)

if __name__ == "__main__":
    main()