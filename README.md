# Discord Daily Bot
A simple Discord bot that posts something new every day — automatically.  

## Features
- Automatically sends a daily image at a specific time  

## Setup
### 1. Clone repository

``` bash
git clone https://github.com/zenru1117/discord-daily-bot.git
cd discord-daily-bot
```

### 2. Install dependencies
``` bash
pip install -r requirements.txt
```
>⚠️ If using Windows, please remove or comment out any `uvloop`-related code in `main.py`

### 3. Configure environment variables
Create a .env file in the root directory:
``` ini
BOT_TOKEN="Your-bot-token"
TARGET_CHANNEL_ID=Target_channel_id
MAX_HISTORY_SIZE=Max_history_size
TIMEZONE="Your-time-zone"

TEST_GUILD_ID=Test_guild_id(Optional)
```

### 4. Run bot
``` bash
# Linux/macOS
python3 main.py

# Windows
py main.py
```

## Used Open Source Project
- [uvloop](https://github.com/MagicStack/uvloop)
- [discord.py](https://github.com/Rapptz/discord.py)

## License
Discord Daily Bot is licensed under MIT.