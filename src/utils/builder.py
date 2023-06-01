import os

from discord import Intents

from bot.yobot import YoBot
from utils.logger import YoBotLogger
from utils.yobotlib import download_cogs, verify_all_cogs, load_config


class YoBotBuilder(YoBot):
    """
    The YoBotBuilder class is used to build a new instance of the YoBot class.
    
    Attributes:
        yobot (YoBot): The YoBot instance.
        config_file (str): The path to the config file.
    """
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = load_config(self.config_file)
        self.log_file = self.config['file_paths']['log_file']
        self.avatar_file = self.config['file_paths']['avatar_file']
        self.cogs_dir = self.config['file_paths']['cogs_dir']
        self.cogs_key_file = self.config['file_paths']['cogs_key_file']
        self.cogs_sigs_dir = self.config['file_paths']['cogs_sigs_dir']
        self.log = YoBotLogger(name='YoBot', log_file=self.log_file, level=self.config['log_level'], maxBytes=1000000, backupCount=1) # Setup the logger.   


    def setup_cogs(self):
        """Downloads the selected cogs from the YoBot repository if the option is selected."""
        self.log.info('Launching YoBot...')
        self.log.debug('Building YoBot instance...')
        try:
            self.log.debug('Checking for cogs directory...')
            if not os.path.isdir(self.cogs_dir):
                self.log.warning('Cogs directory not found. Creating cogs directory...')
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
                    download_cogs(self, self.cogs_dir, self.cogs_sigs_dir) 
                    self.log.info('Cog installation complete.')
        except FileNotFoundError as e:
            self.log.error(f'Error setting up YoBot cogs: {e}')
        except Exception as e:
            self.log.error(f'Error setting up YoBot cogs: {e}')
            self.log.warning('Failed to setup cogs. Continuing without cogs...')


    def yobot_build(self):
        """The build method builds a new instance of the YoBot class.

        Returns:
            YoBot: A newly prepared instance of the YoBot class.
        """
        self.log.debug('Verifying the YoBot instance...')
        try:
            self.setup_cogs()
            if self.config['dev_mode'] == True: # Skip signature check if dev_mode is enabled. 
                self.log.info('Dev mode is enabled. Skipping cog verification.')
                self.log.warning('WARNING: This can allow malicious code to run on your system!')        
            else:
                self.log.debug('Dev mode is not enabled. Verifying cogs...')
                
                if verify_all_cogs(self, self.cogs_dir, self.cogs_key_file, self.config['blacklist']['cog_verify']) == False: # Verify all cogs against their signatures to ensure they have not been tampered with.
                    self.log.warning('YoBot has detected that one or more cogs have been tampered with.')
                    self.log.warning('This can be caused by a malicious user or a bug in the YoBot code.')
                    self.log.warning('If you are a user, please contact the Cog author or the developer of your YoBot.')
                    self.log.warning('If you are a developer, you can disable this check by enabling dev_mode in the config file.')
                    self.log.critical('WARNING: Disabling this check can allow malicious code to run on your system!')
                    self.log.critical('WARNING: Only disable this check if you are a developer and know what you are doing!')
                    input('Press ENTER to EXIT.')
                    exit()
            
            self.log.debug('YoBot setting up intents...')
            intents = Intents.default() # Set Discord intents.
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
