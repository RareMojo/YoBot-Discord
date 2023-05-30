import asyncio
import json
import os
from typing import TYPE_CHECKING

from discord.ext import commands

from utils.logger import terminal_command_loop

if TYPE_CHECKING:
    from discord import Intents

    from utils.logger import YoBotLogger


class YoBot(commands.Bot):
    """Main YoBot class that handles the bot's initialization and startup."""
    def __init__(self: 'YoBot', intents: 'Intents', config_file: str, avatar: str, cogs_dir: str, logger: 'YoBotLogger'):
        
        with open(config_file, 'r') as f: # Ensure that the config file loads before the bot fully starts.
            self.config = json.load(f)
            
        super().__init__(command_prefix=self.config['prefix'], intents=intents)
        """Initializes the bot."""
        self.running = True
        self.config_file = config_file
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
        yobot_task = asyncio.create_task(self.start(self.config['discord_token']))
        command_task = asyncio.create_task(terminal_command_loop(self))
        self.log.info('YoBot starting...')
        try:
            while self.running:
                await asyncio.sleep(0)
        except Exception as e:
            self.log.error(f"Bot encountered an error: {e}")
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
        cog_name = None
        try:
            for filename in os.listdir(self.cogs_dir):
                if filename.endswith('cog.py'):
                    cog_name = f'cogs.{filename[:-3]}'
                    await self.load_extension(cog_name)
                    self.log.info(f'Detected {filename[:-3]}')
                    loaded_extensions += 1
        except Exception as e:
            self.log.error(f'Failed to load extension {cog_name}.')
            self.log.error(f'Error: {e}')
                
        self.log.info('Loaded extensions.')



    def __call__(self, *args, **kwargs) -> 'YoBot':
        return self