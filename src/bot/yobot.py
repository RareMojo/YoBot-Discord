import asyncio
import json
import os

from discord.ext import commands

from utils.logger import terminal_command_loop


class YoBot(commands.Bot):
    """Main YoBot class that handles the bot's initialization and startup.

    Attributes:
        config (dict): The bot's configuration file.
        config_file (str): The path to the bot's configuration file.
        avatar (str): The path to the bot's avatar file.
        cogs_dir (str): The path to the bot's cogs directory.
        bot_name (str): The bot's name.
        presence (str): The bot's presence.
        owner_name (str): The bot owner's name.
        log (YoBotLogger): The bot's logger.
        running (bool): The bot's running flag.
        """
    def __init__(self, intents, logger, config_file, avatar, cogs_dir):
        with open(config_file, 'r') as f: # Make sure the config file is loaded before the bot is fully initialized.
            self.config = json.load(f)
        super().__init__(command_prefix=self.config['prefix'], intents=intents)
        self.running = True
        self.config_file = config_file # Accessible by calling self.config_file, or yobot.config_file.
        self.avatar = avatar
        self.cogs_dir = cogs_dir
        self.bot_name = self.config['bot_name']
        self.presence = self.config['presence']
        self.owner_name = self.config['owner_name']
        self.owner_id = self.config['owner_id']
        self.log = logger


    async def start_bot(self):
        """Starts YoBot."""
        await self.load_cogs()
        yobot_task = asyncio.create_task(self.start(self.config['discord_token'])) # Start the bot asynchronously.
        command_task = asyncio.create_task(terminal_command_loop(self)) # Start the terminal command loop asynchronously.
        self.log.info('YoBot starting...')
        try:
            while self.running:
                await asyncio.sleep(0)
        except Exception as e:
            self.log.error(f"Bot encountered an error: {e}", level=2)
        finally:
            yobot_task.cancel()
            command_task.cancel()

    def stop_bot(self):
        """Stops YoBot."""
        self.log.info('YoBot stopping...')
        self.running = False
        

    async def load_cogs(self):
        """Loads all cogs in the cogs directory."""
        self.log.info("Loading extensions...")
        loaded_extensions = 0
        for filename in os.listdir(self.cogs_dir):
            if filename.endswith('cog.py'):
                cog_name = f'cogs.{filename[:-3]}'
                await self.load_extension(cog_name)
                self.log.info(f'Detected {filename[:-3]}')
                loaded_extensions += 1
            
        self.log.info('Loaded all extensions.')