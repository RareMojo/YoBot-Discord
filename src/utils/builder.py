import os

from discord import Intents

from bot.yobot import YoBot
from utils.logger import YoBotLogger
from utils.yobotlib import download_cogs, load_config


class Builder(YoBot):
    """
    The Builder class is used to build a new instance of the YoBot class.

    Attributes:
        yobot (YoBot): The YoBot instance.
        config_file (str): The path to the config file.
        config (dict): The config file.
        log_file (str): The path to the log file.
        avatar_file (str): The path to the avatar file.
        cogs_dir (str): The path to the cogs directory.
        repo_info (dict): The repository information.
        log (YoBotLogger): The YoBot logger.
    """

    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = load_config(self.config_file)
        self.log_file = self.config['file_paths']['log_file']
        self.avatar_file = self.config['file_paths']['avatar_file']
        self.cogs_dir = self.config['file_paths']['cogs_dir']
        self.repo_info = self.config['repo_info']
        self.log = YoBotLogger(name='YoBot', log_file=self.log_file,
                               level=self.config['log_level'], maxBytes=1000000, backupCount=1) # Setup the logger.

    def setup_cogs(self):
        """Downloads the selected cogs from the YoBot repository if the option is selected."""
        self.log.info('Launching YoBot...')
        self.log.debug('Building YoBot instance...')
        try:
            self.log.debug('Checking for cogs directory...')
            if not os.path.isdir(self.cogs_dir):
                self.log.warning(
                    'Cogs directory not found. Creating cogs directory...')
                os.mkdir(self.cogs_dir)
            else:
                self.log.debug('Cogs directory found.')
                if not self.config_file:
                    self.log.error('Config file not found.')
                    return

                config = load_config(self.config_file)

                if config['update_bot']:
                    self.log.debug('Trying to build cogs')
                    self.log.info('Running first time Cog installation...')
                    download_cogs(self, self.cogs_dir, self.repo_info)
                    self.log.info('Cog installation complete.')
        except FileNotFoundError as e:
            self.log.error(f'Error setting up YoBot cogs: {e}')
        except Exception as e:
            self.log.error(f'Error setting up YoBot cogs: {e}')
            self.log.warning(
                'Failed to setup cogs. Continuing without cogs...')

    def yobot_build(self):
        """The build method builds a new instance of the YoBot class.

        Returns:
            YoBot: A newly prepared instance of the YoBot class.
        """
        self.log.debug('Verifying the YoBot instance...')
        try:
            self.setup_cogs()
            self.log.debug('YoBot setting up intents...')
            intents = Intents.default()  # Set Discord intents.
            intents.message_content = True
            intents.members = True
            self.log.debug(f'YoBot intents set to {intents}.')
            self.log.debug('YoBot building...')
            return YoBot(
                intents=intents,
                config_file=self.config_file,
                logger=self.log
            )

        except FileNotFoundError as e:
            self.log.error(f'Error building YoBot: {e}')
        except Exception as e:
            self.log.error(f'Error building YoBot: {e}')
            self.log.warning('Failed to build YoBot. Shutting down...')
