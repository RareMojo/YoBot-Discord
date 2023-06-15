import os

from discord import Intents

from bot.yobot import YoBot
from utils.yobot_logger import YoBotLogger
from utils.yobot_lib import download_cogs
from utils.yobot_exceptions import *
from utils.yobot_configs import Configs


class Builder(YoBot):
    """
    The Builder class is used to build a new instance of the YoBot class.

    Attributes:
        yobot (YoBot): The YoBot instance.
        config_file (str): The path to the config file.
        config (Config): The config file.
        log_file (str): The path to the log file.
        avatar_file (str): The path to the avatar file.
        cogs_dir (str): The path to the cogs directory.
        repo_info (dict): The repository information.
        log (YoBotLogger): The YoBot logger.
    """

    def __init__(self, config: Configs):
        self.config = config
        self.config_file = self.config.get('file_paths.config_file')
        self.logo_file = self.config.get('file_paths.ascii_logo')
        self.log_file = self.config.get('file_paths.log_file')
        self.avatar_file = self.config.get('file_paths.avatar_file')
        self.cogs_dir = self.config.get('file_paths.cogs_dir')
        try:
            self.log = YoBotLogger(name='YoBot', log_file=self.log_file,
                                level=self.config.get('log_level'), maxBytes=1000000, backupCount=1) # Setup the logger.
        except OSError as e:
            raise LoggerException(self.log_file, e)
        try:
            with open(self.logo_file, 'r') as logo:
                self.logo = logo.read()
        except OSError as e:
            raise FileException(self.logo_file, e)
        
        green = '\033[92m'
        reset = '\033[0m'
        self.log.info('\n' + green + self.logo + reset + '\n')

    def setup_cogs(self):
        """Downloads the selected cogs from the YoBot repository if the option is selected."""
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

                config = self.config.get('cog_repo')
                update = self.config.get('update_bot')

                if update:
                    self.log.debug('Trying to build cogs')
                    self.log.info('Running first time Cog setup...')
                    download_cogs(self, config['repo_owner'], config['repo_name'], config['repo_info'])
                    self.log.info('Cog setup complete.')
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
                config=self.config,
                logger=self.log
            )

        except FileNotFoundError as e:
            self.log.error(f'Error building YoBot: {e}')
        except Exception as e:
            self.log.error(f'Error building YoBot: {e}')
            self.log.warning('Failed to build YoBot. Shutting down...')
