import asyncio
import os
from typing import TYPE_CHECKING

import yaml
from discord.ext import commands

from utils.yobot_configs import Configs
from utils.yobot_exceptions import *
from utils.yobot_logger import terminal_command_loop

if TYPE_CHECKING:
    from discord import Intents

    from utils.yobot_logger import YoBotLogger


class YoBot(commands.Bot):
    """Main YoBot class that handles the bot's initialization and startup.

    Attributes:
        config (dict): The bot's config file.
        config_file (str): The path to the config file.
        avatar_file (str): The path to the avatar file.
        cogs_dir (str): The path to the cogs directory.
        bot_name (str): The bot's name.
        presence (str): The bot's presence.
        owner_name (str): The bot owner's name.
        owner_id (str): The bot owner's ID.
        log_file (str): The path to the log file.
        log (YoBotLogger): The bot's logger.
        repo_info (str): The bot's repo info.
        cog_removal_blacklist (list): The cog removal blacklist.
        running (bool): Whether the bot is running.
    """

    def __init__(self, intents: 'Intents', config: Configs, logger: 'YoBotLogger'):
        self.config_file = config
        try:
            self.config_file.load  # Ensure this is loaded first.
        except yaml.YAMLError as e:
            raise ConfigException(self.config_file, e)
        self.log_file = self.config_file.get('file_paths.log_file')
        self.log = logger
        self.log.debug('YoBot built.')

        super().__init__(command_prefix=self.config_file.get('prefix'), intents=intents)
        """Initializes the bot."""
        self.log.debug('YoBot initialized.')
        self.running = True
        self.cogs_dir = self.config_file.get('file_paths.cogs_dir')
        self.cogs_removal_blacklist = self.config_file.get('blacklist.cog_removal')
        self.avatar_file = self.config_file.get('file_paths.avatar_file')
        self.bot_name = self.config_file.get('bot_name')
        self.presence = self.config_file.get('presence')
        self.owner_name = self.config_file.get('owner_name')
        self.owner_id = self.config_file.get('owner_id')

    async def start_bot(self):
        """Starts YoBot."""
        self.log.info('YoBot starting...')
        await self.load_cogs()
        # This is for the bot itself.
        yobot_task = asyncio.create_task(
            self.start(self.config_file.get('discord_token')), name='yobot')
        # This is for the terminal commands.
        command_task = asyncio.create_task(terminal_command_loop(self), name='terminal')
        # This is for Flask to run the web server.
        #flask_task = asyncio.create_task(start_server(self))
        try:
            while self.running:
                # This is to allow the bot to run in the background.
                await asyncio.sleep(0)
        except Exception as e:
            self.log.error(f"Bot encountered an error: {e}")
        finally:
            yobot_task.cancel()  # Cancels the bot task.
            command_task.cancel()  # Cancels the command task.
            #flask_task.cancel()  # Cancels the Flask task.

    def stop_bot(self):
        """Stops YoBot."""
        self.log.info('YoBot stopping...')
        self.running = False

    async def load_cogs(self):
        """Loads all cogs in the cogs directory."""
        self.log.debug("Loading cogs...")
        loaded_extensions = 0
        cog_name = None
        try:
            for filename in os.listdir(self.cogs_dir):
                if filename.endswith('cog.py'):
                    cog_name = f'cogs.{filename[:-3]}'
                    if cog_name in self.extensions:
                        self.log.debug(
                            f'Skipping - [ {filename[:-3]} ] (already loaded)')
                        continue
                    await self.load_extension(cog_name)
                    self.log.debug(f'Loaded - [ {filename[:-3]} ]')
                    loaded_extensions += 1
        except Exception as e:
            raise CogException(cog_name, f'There was an error loading {e}')
        self.log.debug(f'Loaded {loaded_extensions} cogs.')