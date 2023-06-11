import collections.abc
import logging
import traceback
from typing import TYPE_CHECKING

import discord
import requests
import yaml

if TYPE_CHECKING:
    from bot.yobot import YoBot


async def welcome_to_yobot(yobot: 'YoBot') -> None:
    """
    Prints a welcome message to the terminal.

    Args:
        yobot (YoBot): The bot instance.
    """
    try:
        yobot.log.debug('Starting welcome_to_yobot function...')
        yobot.log.info('YoBot Instance Details:')
        yobot.log.info('Display name: {}'.format(yobot.bot_name))
        yobot.log.info('Presence: {}'.format(yobot.presence))

        for guild in yobot.guilds:  # Print the guilds YoBot is connected to.
            yobot.log.info(f'Linked with {guild} | ID: {guild.id}')

        yobot.log.info('YoBot is online and ready.')
        # If this is not the first run, print a welcome back message.
        if not yobot.config['update_bot']:
            yobot.log.info('Welcome back to YoBot, {}!'.format(
                yobot.config['owner_name']))
            yobot.log.info('Type "help" for a list of terminal commands.')

        else:  # If this is the first run, print a welcome message.
            yobot.log.info('Welcome to YoBot, {}!'.format(
                yobot.config['owner_name']))
            yobot.log.info(
                'Be sure to check out the documentation at the GitHub repository.')
            yobot.log.info(
                'If you ever want to design a cog, check out the YoBot-Discord-Cog GitHub repository.')
            yobot.log.info('Type "help" for a list of terminal commands.')

    except Exception as e:
        yobot.log.error(f'Error in welcome_to_yobot function: {e}')


async def update_yobot(yobot: 'YoBot') -> None:
    """
    Updates YoBot's name, presence, and avatar to config values on Discord servers.

    Args:
        yobot (YoBot): The bot instance.
    """
    config_file = yobot.config_file
    successful = True  # Whether or not the update was successful.
    yobot.log.debug('Starting update_yobot function...')
    yobot.log.debug('Checking for updates to YoBot settings...')

    if yobot.config['update_bot'] == True:
        yobot.log.info('First run or changes detected!')
        yobot.log.info('Setting name, presence, and avatar to config values.')
        yobot.log.warning(
            'This action is rate limited, so to change it later, edit the config file.')
        yobot.log.warning(
            'You may also manually set these attributes with the terminal.')

        try:  # Try to update the bot's name, presence, and avatar on the Discord servers.
            with open(yobot.avatar_file, 'rb') as f:
                new_avatar = f.read()
                await yobot.user.edit(avatar=new_avatar)
            await yobot.user.edit(username=yobot.config['bot_name'])
            await yobot.change_presence(activity=discord.Game(name=yobot.presence))
        except Exception as e:
            yobot.log.error('Error: {}'.format(e))
            yobot.log.error(
                'Failed to synchronize YoBot settings with Discord.')
            yobot.log.warning(
                'Bot name, avatar, or presence not changed on Discord servers.')
            yobot.log.warning('This will be run again on next startup.')
            successful = False

        if successful == True:
            yobot.log.info(
                'Successfully synchronized YoBot settings with Discord.')
            update_config(config_file, {"update_bot": False})
    else:
        yobot.log.info('YoBot settings are up to date.')
        yobot.log.info('Connected to Discord.')
    yobot.log.debug('Exiting update_yobot function...')


def get_boolean_input(yobot: 'YoBot', prompt: str) -> bool:
    """
    Returns a boolean input.

    Args:
        yobot (YoBot): The bot instance.
        prompt (str): The prompt to display.
    """
    while True:
        try:
            user_input = input(prompt)

            if user_input.lower() in ['true', 't', 'yes', 'y']:
                return True

            elif user_input.lower() in ['false', 'f', 'no', 'n']:
                return False

            else:
                yobot.log.warning('Invalid input. Try again.')

        except Exception as e:
            yobot.log.error(f'Error occurred while getting boolean input: {e}')
            yobot.log.debug(f'Error details: {traceback.format_exc()}')
            yobot.log.warning('Invalid input. Try again.')


def github_repo_fetch(yobot: 'YoBot', owner: str, repo: str, repo_dir: str) -> list:
    """
    Fetches a list of files from a repo/directory on GitHub.

    Args:
        owner (str): The owner of the repo.
        repo (str): The name of the repo.
        repo_dir (str): The directory of the repo.    
    """
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{repo_dir}"
        response = requests.get(url)

        if response.status_code == 200:
            files = [file["name"]
                     for file in response.json() if file["type"] == "file"]
            return files
        else:
            yobot.log.debug(
                f"Failed to fetch files from {owner}/{repo}/{repo_dir}. Response status code: {response.status_code}")
            return []
    except Exception as e:
        yobot.log.error(
            f"An error occurred while fetching files from {owner}/{repo}/{repo_dir}: {e}")
        return []


def github_repo_pull(yobot: 'YoBot', owner: str, repo: str, repo_dir: str, target_dir: str) -> None:
    """
    Pulls a repo/directory from GitHub.

    Args:
        yobot (YoBot): The YoBot instance.
        owner (str): The owner of the repo.
        repo (str): The name of the repo.
        repo_dir (str): The directory of the repo.
        target_dir (str): The directory to download the repo to.
    """
    try:
        files = github_repo_fetch(yobot, owner, repo, repo_dir)

        if files:
            for file in files:
                url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/{repo_dir}/{file}"
                response = requests.get(url)

                if response.status_code == 200:
                    with open(f"{target_dir}/{file}", "wb") as f:
                        f.write(response.content)
                    yobot.log.info(f'{file} downloaded.')
                else:
                    yobot.log.error(
                        f'Error downloading {file}. Status code: {response.status_code}')
    except Exception as e:
        yobot.log.error(f'Error downloading files: {e}')
        yobot.log.debug(f'Error details: {traceback.format_exc()}')


def load_config(config_file: str) -> dict:
    """
    Load a YAML configuration file.

    Args:
        config_file (str): The path to the YAML configuration file.

    Returns:
        dict: The configuration settings.
    """
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        logging.warning(f"Config file {config_file} not found.")
        return {}
    except yaml.YAMLError as e:
        logging.warning(f"Error loading config file {config_file}: {e}")
        return {}
    return config


def recursive_update(original, update):
    """
    Recursively updates a dictionary.

    Args:
        original (dict): The original dictionary.
        update (dict): The new dictionary with values to update.
    """
    for key, value in update.items():
        if isinstance(value, collections.abc.Mapping):
            original[key] = recursive_update(original.get(key, {}), value)
        else:
            original[key] = value
    return original


def update_config(config_file: str, updated_values: dict):
    """
    Update a YAML configuration file.

    Args:
        config_file (str): The path to the YAML configuration file.
        updated_values (dict): The new configuration settings.
    """
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        logging.warning(f"Config file {config_file} not found.")
        return
    except yaml.YAMLError as e:
        logging.warning(f"Error loading config file {config_file}: {e}")
        return

    config = recursive_update(config, updated_values)

    try:
        with open(config_file, 'w') as file:
            yaml.safe_dump(config, file, default_flow_style=False)
    except yaml.YAMLError as e:
        logging.warning(f"Error writing to config file {config_file}: {e}")
        return

    logging.debug(f"Config file {config_file} updated with {updated_values}")
    
    
def download_cogs(yobot: 'YoBot', cogs_dir: str, repo_info: dict) -> None:
    """
    Downloads cogs from the terminal. Use for setup or at the user's discretion.

    Args:
        yobot (YoBot): The YoBot instance.
        cogs_dir (str): The directory to download the cogs to.
        sigs_dir (str): The directory to download the sigs to.
    """
    try:
        yobot.log.debug('Starting download_cogs function...')
        get_cogs = get_boolean_input(
            yobot, 'Do you want to download cogs? (y/n) ')
        successful = False

        if get_cogs == True:
            get_all_cogs = get_boolean_input(
                yobot, 'Do you want to download all cogs? (y/n) ')

            if get_all_cogs == True:
                yobot.log.info('Downloading all cogs from the repository...')
                github_repo_pull(
                    yobot, repo_info['repo_owner'], repo_info['repo_name'], repo_info['repo_cogs'], cogs_dir)
            else:
                yobot.log.info(
                    'Fetching the list of cogs from the repository...')
                files = github_repo_fetch(
                    yobot, "RareMojo", "YoBot-Discord-Cogs", "Cogs")

                if files:
                    yobot.log.info('List of cogs available:')
                    for i, file in enumerate(files, start=1):
                        yobot.log.info(f'{i}. {file}')

                    selected_cogs = input(
                        'Enter the numbers of the cogs you want to download (separated by commas): ')
                    selected_cogs = [int(num.strip())
                                     for num in selected_cogs.split(',')]

                    successful = True
                    yobot.log.debug(
                        'Downloading selected cogs and their signatures from the repository...')

                    for cog_index in selected_cogs:
                        cog_name = files[cog_index - 1]
                        url = f"https://raw.githubusercontent.com/RareMojo/YoBot-Discord-Cogs/master/Cogs/{cog_name}"

                        response = requests.get(url)
                        if response.status_code == 200:
                            with open(f"{cogs_dir}/{cog_name}", "wb") as f:
                                f.write(response.content)
                            yobot.log.debug(f'{cog_name} downloaded.')
                        else:
                            yobot.log.error(f'Error downloading {cog_name}.')
                            successful = False
                if successful:
                    yobot.log.debug('Cogs downloaded.')
        else:
            yobot.log.debug('Cogs not downloaded.')
    except Exception as e:
        yobot.log.error(f'Error downloading cogs: {e}')