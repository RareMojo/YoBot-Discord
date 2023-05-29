import json
import os

from discord import Intents

from utils.yobot_logger import YoBotLogger


class YoBotBuilder:
    """
    The YoBotBuilder class is used to build a new instance of the YoBot class.
    
    Attributes:
        yobot (YoBot): The YoBot class to build.
        log_file (str): The path to the log file.
        config_file (str): The path to the config file.
        avatar_file (str): The path to the avatar file.
        cogs_dir (str): The path to the cogs directory.    
    """
    def __init__(self, yobot, log_file, config_file, avatar_file, cogs_dir):
        self.yobot = yobot
        self.config_file = config_file
        self.log_file = log_file
        self.avatar_file = avatar_file
        self.cogs_dir = cogs_dir
        self.log = YoBotLogger('YoBot', self.log_file, level=0, maxBytes=1000000, backupCount=1) # Setup the logger.


    def setup_files(self):
        """Sets up the necessary files for YoBot to run."""
        if not os.path.isdir(self.log_file.rsplit('/', 1)[0]):
            self.log.error('Logs directory not found.')
            self.log.warning('Creating logs directory...')
            os.mkdir(self.log_file.rsplit('/', 1)[0])

        if not os.path.isdir(self.config_file.rsplit('/', 1)[0]):
            self.log.error('Configs directory not found.')
            self.log.warning('Creating configs directory...')
            os.mkdir(self.config_file.rsplit('/', 1)[0])

        self.log.info('YoBot preparing to start...')


    def setup_config(self):
        """
        Sets up the config file for YoBot. 
        
        If the config file is not found, the user will be prompted to enter the necessary information to create the config file.
        """
        if not os.path.isfile(self.config_file):
            self.log.error('Config file not found.')
            self.log.warning('Setting up config...')
            self.log.info('Please enter the following information to set up the config file.')
            config = {}
            config['discord_token'] = input('Discord Token: ')
            config['owner_name'] = input('Owner Name: ')
            config['owner_id'] = input('Owner ID: ')
            config['prefix'] = input('Command Prefix: ')
            config['bot_name'] = input('Display Name: ')
            config['presence'] = input('Presence: ')
            config['debug'] = input('Enable Debug: (True/False) ') # This is a flag to indicate whether or not to enable debug mode.
            config['update_bot'] = True # This is a flag to indicate that YoBot needs to synchronize with the config file.

            with open(self.config_file, 'w') as f: # Save the config file.
                config = json.dumps(config, indent=4)
                f.write(config)
                self.log.info('Config setup complete.')
        else:
            self.log.info('Config file found.')


    def build(self):
        """The build method builds a new instance of the YoBot class.

        Returns:
            YoBot: A newly prepared instance of the YoBot class.
        """
        self.setup_files()
        self.setup_config()

        intents = Intents.default() # Set Discord intents.
        intents.message_content = True
        intents.members = True

        with open(self.avatar_file, 'rb') as f: # Read the avatar file as bytes.
            avatar = f.read()

        return self.yobot(
            logger=self.log,
            intents=intents,
            config_file=self.config_file, # Pass the config file path to YoBot to easily access it.
            avatar=avatar,
            cogs_dir=self.cogs_dir
        )