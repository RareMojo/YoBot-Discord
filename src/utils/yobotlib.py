import configparser
import json
import logging
import os


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',))
LANGUAGE_DEFAULT = os.path.join(ROOT_DIR, 'resources', 'texts', 'system', 'languages', 'EN_system_messages.json')
CORE_CONFIG_FILE = os.path.join(ROOT_DIR, 'configs', 'core_config.ini')
BOT_CONFIG_FILE = os.path.join(ROOT_DIR, 'configs', 'bot_config.ini')
LOG_FILE = os.path.join(ROOT_DIR, 'logs', 'log.txt')
AVATAR_FILE = os.path.join(ROOT_DIR, 'resources', 'images', 'avatar.png')
COGS_DIR = os.path.join(ROOT_DIR, 'src', 'cogs')


def log(msg_key=None, **msg_args):
    """
    Logs a formatted message based on the provided message key and arguments.

    Parameters:
        msg_key (str): The key of the message to be logged.
        **msg_args: Keyword arguments for formatting the message.
    """
    if msg_key:
        if os.path.isfile(CORE_CONFIG_FILE):
            config = get_config('core')
            CURRENT_LANGUAGE = config.get('settings', 'language')
            language = json.loads(open(LANGUAGE_DEFAULT).read())
            language = json.loads(open(CURRENT_LANGUAGE).read())

        message = language.get(msg_key)

        if message is not None:
            if isinstance(message, dict):
                title = message.get('title')
                logging.info(title)
                for sub_key, sub_message in message.items():
                    if sub_key != 'title':
                        try:
                            formatted_sub_message = sub_message.format(**msg_args)
                            logging.info(formatted_sub_message)
                        except KeyError as e:
                            logging.error(f"KeyError: {e}. Message key '{msg_key}' failed to format because {e} key is missing from msg_args.")
            else:
                try:
                    formatted_message = message.format(**msg_args)
                    logging.info(formatted_message)
                except KeyError as e:
                    logging.error(f"KeyError: {e}. Message key '{msg_key}' failed to format because {e} key is missing from msg_args.")
        else:
            logging.info(f"Message key '{msg_key}' not found.")
    else:
        logging.info(msg_args.get('msg', ''))


def get_config(file_path=None):
    """
    Returns the data from a config file.
    
    Parameters:
        file_path (str): The path to the config file.
        Sub for 'bot' and 'core' for their respective config files.
    
    Returns:
        config (configparser.ConfigParser): The data from the config file.
    """
    match file_path:
        case 'bot':
            file_path = BOT_CONFIG_FILE
        case 'core':
            file_path = CORE_CONFIG_FILE

    if os.path.isfile(file_path) and file_path.endswith('.ini'):
        config_file = configparser.ConfigParser()
        config_file.read(file_path)
        return config_file
    else:
        log(msg_key='error', error='Config file does not exist.')


def update_config_file(file_path=None, keys=None):
    """
    Updates the config file without damaging it.
    
    Parameters:
        file_path (str): The path to the config file.
        keys (dict): The data to be saved.
    """
    match file_path:
        case 'bot':
            file_path = BOT_CONFIG_FILE
        case 'core':
            file_path = CORE_CONFIG_FILE

    config = configparser.ConfigParser()
    config.read(file_path)
    
    for section, options in keys.items():
        if not config.has_section(section):
            config.add_section(section)
        
        for option, value in options.items():
            config.set(section, option, value)

    with open(file_path, 'w') as config_file:
        config.write(config_file)


def get_boolean_input(prompt):
    """
    Returns a boolean input.
    
    Parameters:
        prompt (str): The prompt to display.
    """
    while True:
        user_input = input(prompt)
        if user_input.lower() in ['true', 't', 'yes', 'y']:
            return True
        elif user_input.lower() in ['false', 'f', 'no', 'n']:
            return False
        else:
            log(msg_key="error", error=f"Invalid input: {user_input}")


async def sync_commands(yobot):
    """
    Syncs all Cog commands to the Discord bot.
    """
    sync_list = await yobot.tree.sync()
    log(msg='Loaded {} commands.'.format(len(sync_list)))
    return sync_list


async def set_avatar(yobot):
    """
    Sets YoBot's avatar.
    
    Note: Rate limited by the Discord API.

    Call this only when necessary and as few times as possible.
    """
    try:
        with open(AVATAR_FILE, "rb") as f:
            avatar_image = f.read()
        await yobot.user.edit(avatar=avatar_image)
    except Exception as e:
        log(msg_key='error', error=e)
        log(msg='Avatar change will process next restart or reload.')


async def set_display_name(yobot, display_name=None):
    """
    Sets YoBot's display name.
    
    Note: Rate limited by the Discord API.

    Call this only when necessary and as few times as possible.
    """
    if not display_name:
        display_name = get_config('bot').get('settings', 'display_name')

    update = {'settings': {'display_name': display_name}}
    update_config_file('bot', update)

    try:
        await yobot.user.edit(username=display_name)
    except Exception as e:
        log(msg_key='error', error=e)
        log(msg='Name change will process next restart or reload.')

    log(msg='Bot name changed to {}!'.format(display_name))