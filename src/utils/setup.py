import configparser
import logging
import os
from logging.handlers import RotatingFileHandler

from discord import Intents

from .terminal_commands import set_language
from .yobotlib import get_config, log


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',))
LANGUAGES_DIR = os.path.join(ROOT_DIR, 'resources', 'texts', 'system', 'languages')
LANGUAGE_EXTRAS_DIR = os.path.join(ROOT_DIR, 'resources', 'texts', 'system', 'languages', 'extras')
CORE_CONFIG_FILE = os.path.join(ROOT_DIR, 'configs', 'core_config.ini')
BOT_CONFIG_FILE = os.path.join(ROOT_DIR, 'configs', 'bot_config.ini')
LOG_FILE = os.path.join(ROOT_DIR, 'logs', 'log.txt')
AVATAR_FILE = os.path.join(ROOT_DIR, 'resources', 'images', 'avatar.png')
COGS_DIR = os.path.join(ROOT_DIR, 'src', 'cogs')
EVENTS_DIR = os.path.join(ROOT_DIR, 'src', 'events')


def setup_logging():
    """Sets up the logging module."""
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%m-%d-%Y %H:%M:%S')

    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=2000, backupCount=1)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    log(msg_key='success', success='Console setup')


def setup_files():
    """Sets up the required file structure."""
    if not os.path.isdir('../logs'):
        log(msg_key='error', error='Logs directory not found.')
        log(msg='Creating logs directory...')
        os.mkdir('../logs')
    
    if not os.path.isdir('../data'):
        log(msg_key='error', error='Data directory not found.')
        log(msg='Creating data directory...')
        os.mkdir('../data')

    log(msg_key='success', success='File creation')


def setup_core_config():
    """Sets up the core config."""
    if os.path.isfile(CORE_CONFIG_FILE):
        log(msg_key='loaded', loaded='Core Config')
        return None

    log(msg_key='setup_wizard')

    core = {}
    core['owner_name'] = input('Owner Name: ')
    core['debug'] = input('Enable Debug: (True/False) ')
    core['language'] = set_language()

    data = {'settings': core}

    config = configparser.ConfigParser()
    for section, section_data in data.items():
        config[section] = section_data
        with open(CORE_CONFIG_FILE, 'w') as file:
            config.write(file)

    log(msg_key='success', success='Core Setup Wizard')


def setup_bot_config():
    """Sets up the Discord bot config."""
    if os.path.isfile(BOT_CONFIG_FILE):
        log(msg_key='loaded', loaded='Bot Config')
        return
    
    log(msg_key='setup_wizard')

    bot_keys = {}
    discord_token = input('Discord API Key: ')
    bot_keys['discord_token'] = discord_token

    bot_settings = {}
    bot_settings['display_name'] = input('Bot Display Name: ')
    bot_settings['now_playing'] = input('Now Playing Message (optional): ')
    bot_settings['first_run'] = True

    bot_intents = {}
    bot_intents['all'] = input('All Intents (True/False): ')

    bot_intents['all'] = bool(bot_intents['all'])
    if not bot_intents['all'] or bot_intents['all'] == False:
        bot_intents['default'] = bool(bot_intents['default'])

    data = {'keys': bot_keys, 'settings': bot_settings, 'intents': bot_intents}
    
    config = configparser.ConfigParser()
    for section, section_data in data.items():
        config[section] = section_data
        with open(BOT_CONFIG_FILE, 'w') as file:
            config.write(file)

    log(msg_key='success', success='Bot Setup Wizard')


def set_intents():
    """Sets the Discord intents based on the Discord bot_config.ini."""
    user_intents = get_config('bot')
    intents = Intents.default()
    intents.message_content = True

    if user_intents.getboolean('intents', 'all'):
        intents = Intents.all()

    return intents


async def setup_cogs(yobot):
    """
    Loads all cogs and events from the cogs/events directory.

    Args:
        bot (YoBot): The bot instance
    """
    log(msg="Loading extensions...")
    loaded_extensions = 0

    for filename in os.listdir(COGS_DIR):
        if filename.endswith('cog.py'):
            cog_name = f'cogs.{filename[:-3]}'
            await yobot.load_extension(cog_name)
            loaded_extensions += 1

    for filename in os.listdir(EVENTS_DIR):
        if filename.endswith('events.py'):
            event_name = f'events.{filename[:-3]}'
            await yobot.load_extension(event_name)
            loaded_extensions += 1
    
    for filename in os.listdir(COGS_DIR):
        if filename.endswith('cog.py'):
            log(msg_key='loaded', loaded=f"[{filename[:-3]}]")
    
    for filename in os.listdir(EVENTS_DIR):
        if filename.endswith('events.py'):
            log(msg_key='loaded', loaded=f"[{filename[:-3]}]")

    log(msg=f"Total extensions loaded: {loaded_extensions}")


def setup_bot(yobot):
    """
    Sets up YoBot.
    This is to be called from the main.py file.

    Args:
        bot (YoBot): The bot class

    Returns:
        YoBot: The bot instance
    """
    setup_files()
    setup_core_config()
    setup_bot_config()
    setup_logging()

    config = get_config('bot')
    intents = set_intents()

    with open(AVATAR_FILE, "rb") as f:
        avatar_image = f.read()

    return yobot(
        intents=intents,
        display_name=config["settings"]["display_name"],
        now_playing=config["settings"]["now_playing"],
        discord_token=config["keys"]["discord_token"],
        avatar=avatar_image
    )