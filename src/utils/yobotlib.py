import collections.abc
import hashlib
import logging
import os
import traceback
from typing import TYPE_CHECKING, Union

import discord
import requests
import yaml
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.serialization import load_pem_public_key

if TYPE_CHECKING:
    from bot.yobot import YoBot


def show_help(yobot: 'YoBot') -> None:
    """
    Shows the help menu.

    Args:
        yobot (YoBot): The bot instance.
    """
    black = '\033[30m'
    cyan = '\033[36m'
    green = '\033[32m'
    purple = '\033[35m'
    bold = '\033[1m'
    reset = '\033[0m'
    commands = {
        'exit': 'Shuts YoBot and the script down.',
        'help': 'Displays this message.',
        'ping': 'Pongs.',
        'setbotname': 'Changes the current YoBot name.',
        'setbotpresence': 'Changes the current YoBot presence.',
        'setbotavatar': 'Changes the current YoBot avatar.',
        'setowner': 'Sets the owner of the bot.',
        'reload': 'Synchronizes commands with Discord.',
        'wipebot': 'Wipes the bot\'s configuration files.',
        'getcog': 'Downloads and loads cogs.',
        'removecog': 'Removes cogs from the bot.',
        'listcogs': 'Lists all cogs currently loaded.',
        'verifycogs': 'Verifies the integrity of cogs.',
        'aliases': 'Lists all command aliases.',
        'debug': 'Toggles debug mode.',
        'devmode': 'Toggles developer mode.',
        'addblacklist': 'Adds a cog to the blacklist.',
        'removeblacklist': 'Removes a cog from the blacklist.',
    }
    try:
        yobot.log.debug('Starting show_help function...')
        yobot.log.info(
            f"{black}{'-' * 24}[ {purple}{bold}Available commands{reset}{black} ]{'-' * 24}{reset}")
        yobot.log.info('')
        yobot.log.info(
            f"{cyan}Simply type the command you want to execute and press enter.{reset}")
        yobot.log.info(
            f"{cyan}A brief description of the command will be displayed below.{reset}")
        yobot.log.info('')

        for command, description in commands.items():
            yobot.log.info(
                f"{green}{command}{' ' * (30 - len(command))}{black}- {description}{' ' * (45 - len(description))}{reset}")
        yobot.log.info('')
        yobot.log.info(
            f"{black}{'-' * 22}[ {purple}{bold}End available commands{reset}{black} ]{'-' * 22}{reset}")
        yobot.log.debug('Exiting show_help function...')
    except Exception as e:
        yobot.log.error(f"Error in show_help function: {e}")
        traceback.print_exc()


def show_aliases(yobot: 'YoBot') -> None:
    """
    Shows the aliases for YoBot's commands.

    Args:
        yobot (YoBot): The bot instance.
    """
    black = '\033[30m'
    green = '\033[32m'
    purple = '\033[35m'
    bold = '\033[1m'
    reset = '\033[0m'
    aliases = {
        'exit': ['quit', 'shutdown'],
        'help': ['h', '?'],
        'ping': ['p'],
        'setbotname': ['setbot', 'sbn'],
        'setbotpresence': ['setbotpres', 'sbp'],
        'setbotavatar': ['setava', 'sba'],
        'setowner': ['setown'],
        'reload': ['sync', 'r'],
        'wipebot': ['wipeconfig', 'wipe', 'wb'],
        'getcog': ['getcogs', 'gc'],
        'removecog': ['removecogs', 'rc'],
        'listcogs': ['list', 'lc'],
        'alias': ['aliases', 'a'],
        'debug': ['d'],
        'developer': ['dev', 'devmode', 'dm'],
        'verifycogs': ['verify', 'vc'],
        'addblacklist': ['addbl', 'abl'],
        'removeblacklist': ['rmblist', 'rmbl'],
    }
    try:
        yobot.log.debug('Starting show_aliases function...')
        yobot.log.info(
            f"{black}{'-' * 24}[ {purple}{bold}Command Aliases{reset}{black} ]{'-' * 24}{reset}")
        yobot.log.info('')

        for command, alias_list in aliases.items():
            aliases_str = ', '.join(alias_list)
            yobot.log.info(
                f"{green}{command}{' ' * (30 - len(command))}{black}- {aliases_str}{' ' * (45 - len(aliases_str))}{reset}")
        yobot.log.info('')
        yobot.log.info(
            f"{black}{'-' * 22}[ {purple}{bold}End command aliases{reset}{black} ]{'-' * 22}{reset}")
        yobot.log.debug('Exiting show_aliases function...')
    except Exception as e:
        yobot.log.error(f"Error in show_aliases function: {e}")
        traceback.print_exc()


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


async def welcome_to_yobot(yobot: 'YoBot') -> None:
    """
    Prints a welcome message to the terminal.

    Args:
        yobot (YoBot): The bot instance.
    """
    try:
        yobot.log.debug('Starting welcome_to_yobot function...')
        yobot.log.info('YoBot Instance Details:')
        # Print YoBot's current display name.
        yobot.log.info('Display name: {}'.format(yobot.bot_name))
        # Print YoBot's current presence.
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


def exit_bot_terminal(yobot: 'YoBot') -> None:
    """
    Shutsdown YoBot from the terminal.

    Args:
        yobot (YoBot): The bot instance.
    """
    try:
        yobot.log.debug('Shutting down YoBot...')
        yobot.stop_bot()
    except Exception as e:
        yobot.log.error(f'Error shutting down YoBot: {e}')


async def set_bot_name(yobot: 'YoBot') -> None:
    """
    Changes YoBot's name from the terminal.

    This updates the config file and Discord servers.

    Args:
        yobot (YoBot): The YoBot instance.
    """
    try:
        yobot.log.debug('Setting bot name...')
        yobot.log.info(f'Current name: {yobot.config["bot_name"]}')
        change_bot_name = get_boolean_input(
            yobot, 'Do you want to change YoBots name? (y/n) ')

        if change_bot_name == True:
            new_name = input('Enter new bot name: ')
            try:
                await yobot.user.edit(username=new_name)
                yobot.log.info(
                    'Config change, bot_name: {} -> {}'.format(yobot.config['bot_name'], new_name))
                update_config(yobot.config_file, {
                              "bot_name": new_name, "update_bot": True})
            except Exception as e:
                yobot.log.error('Error: {}'.format(e))
                yobot.log.warning('Bot name not changed on Discord servers.')
        else:
            yobot.log.info('Name not changed.')
    except Exception as e:
        yobot.log.error('Error: {}'.format(e))
        traceback.print_exc()


async def set_bot_avatar(yobot: 'YoBot') -> None:
    """
    Changes YoBot's avatar from the terminal.

    This updates the config file and Discord servers.

    Args:
        yobot (YoBot): The YoBot instance.
    """
    try:
        yobot.log.debug('Setting bot avatar...')
        yobot.log.info(
            'This sets the avatar to the image at ../resources/images/avatar.png')
        change_avatar = get_boolean_input(
            yobot, 'Do you want to change the avatar? (y/n) ')
        successful = True

        with open(yobot.avatar_file, 'rb') as f:
            new_avatar = f.read()

        if change_avatar == True:
            try:
                await yobot.user.edit(avatar=new_avatar)
            except Exception as e:
                yobot.log.error('Error: {}'.format(e))
                yobot.log.warning('Avatar not changed on Discord servers.')
                yobot.log.warning(
                    'It will automatically be changed on the next startup.')
                successful = False

            if successful == False:
                update_config(yobot.config_file, {"update_bot": True})

            if successful == True:
                yobot.log.info('Avatar changed.')
        else:
            yobot.log.info('Avatar not changed.')

    except Exception as e:
        yobot.log.error('Error: {}'.format(e))


async def set_bot_presence(yobot: 'YoBot') -> None:
    """
    Changes YoBot's presence from the terminal.

    This updates the config file and Discord servers.

    Args:
        yobot (YoBot): The YoBot instance.
    """
    try:
        yobot.log.info('Current presence: {}'.format(yobot.presence))
        update_presence = get_boolean_input(
            yobot, 'Do you want to change the presence? (y/n) ')

        if update_presence == True:
            new_presence = input('Enter new presence: ')
            update_config(yobot.config_file, {
                          "presence": new_presence, "update_bot": True})

            try:
                # Try to change the presence on Discord servers.
                await yobot.change_presence(activity=discord.Game(name=new_presence))
                yobot.log.info(
                    'Config change, presence: {} -> {}'.format(yobot.presence, new_presence))
            except Exception as e:
                yobot.log.error('Error: {}'.format(e))
                yobot.log.warning('Presence not changed.')
        else:
            yobot.log.info('Presence not changed.')
    except Exception as e:
        yobot.log.debug(f'Error in set_bot_presence: {traceback.format_exc()}')
        yobot.log.error(f'Error in set_bot_presence: {e}')


async def sync_commands(yobot: 'YoBot') -> None:
    """
    Synchronizes YoBot's commands from the terminal.

    Args:
        yobot (YoBot): The YoBot instance.
    """
    try:
        synchronize = get_boolean_input(
            yobot, 'Do you want to synchronize commands? (y/n) ')

        if synchronize == True:
            # Try to update commands on Discord servers.
            sync_list = await yobot.tree.sync()
            yobot.log.info(f'{len(sync_list)} commands synchronized.')
        else:
            yobot.log.info('Commands not synchronized.')
    except Exception as e:
        yobot.log.debug(f'Error in sync_commands: {traceback.format_exc()}')
        yobot.log.error(f'Error in sync_commands: {e}')
        yobot.log.error('Commands not synchronized.')


async def set_owner(yobot: 'YoBot') -> None:
    """
    Changes YoBot's owner from the terminal.

    This updates the config file and the respected admin of YoBot.

    Args:
        yobot (YoBot): The YoBot instance.
    """
    try:
        yobot.log.info(
            f'Current owner: {yobot.config["owner_name"]} - {yobot.config["owner_id"]}')
        change_owner_name = get_boolean_input(
            yobot, 'Do you want to change YoBots owner? (y/n) ')

        if change_owner_name == True:
            new_owner_name = input('Enter new owner name: ')
            new_owner_id = input('Enter new owner id: ')

            update_config(yobot.config_file, {
                          "owner_name": new_owner_name, "owner_id": new_owner_id})

            yobot.log.info(
                'Config change, owner_name: {} -> {}'.format(yobot.config['owner_name'], new_owner_name))
            yobot.log.info(
                'Config change, owner_id: {} -> {}'.format(yobot.config['owner_id'], new_owner_id))
        else:
            yobot.log.info('Owner not changed.')
    except Exception as e:
        yobot.log.debug(f'Error in set_owner function: {e}')
        yobot.log.error(f'Error in set_owner function: {e}')


def ping(yobot: 'YoBot') -> None:
    """Pong!"""
    try:
        yobot.log.debug('Pinging...')
        yobot.log.info('Pong!')
    except Exception as e:
        yobot.log.error(f'Error in ping function: {e}')


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


def wipe_config(yobot: 'YoBot') -> None:
    """
    Wipes the config file and shuts down YoBot, causing setup to run on next startup

    Args:
        yobot (YoBot): The bot instance.
    """
    try:
        yobot.log.warning(
            'This will wipe the config file and shut down YoBot.')
        wipe = get_boolean_input(
            yobot, 'Do you want to wipe the config file? (y/n) ')

        if wipe == True:
            wipe_confirm = get_boolean_input(
                yobot, 'Are you sure you want to wipe config and restart? (y/n) ')

            if wipe_confirm == True:
                os.remove(yobot.config_file)
                yobot.log.info('Config file wiped.')
                yobot.log.warning('YoBot will now shut down.')
                exit_bot_terminal(yobot)
            else:
                yobot.log.info('Config file not wiped.')
        else:
            yobot.log.info('Config file not wiped.')
    except FileNotFoundError as e:
        yobot.log.debug(f"Config file not found: {e}")
    except Exception as e:
        yobot.log.error(f"An error occurred while wiping the config file: {e}")


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


def download_cogs(yobot: 'YoBot', cogs_dir: str, sigs_dir: str, repo_info: dict) -> None:
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
                github_repo_pull(
                    yobot, repo_info['repo_owner'], repo_info['repo_name'], repo_info['repo_sigs'], sigs_dir)
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
                        sig_url = f"https://raw.githubusercontent.com/RareMojo/YoBot-Discord-Cogs/master/Sigs/{cog_name}.sig"

                        response = requests.get(url)
                        if response.status_code == 200:
                            with open(f"{cogs_dir}/{cog_name}", "wb") as f:
                                f.write(response.content)
                            yobot.log.debug(f'{cog_name} downloaded.')
                        else:
                            yobot.log.error(f'Error downloading {cog_name}.')

                        sig_response = requests.get(sig_url)
                        if sig_response.status_code == 200:
                            with open(f"{sigs_dir}/{cog_name}.sig", "wb") as f:
                                f.write(sig_response.content)
                            yobot.log.debug(f'{cog_name}.sig downloaded.')
                        else:
                            yobot.log.error(
                                f'Error downloading {cog_name}.sig.')

                if successful:
                    yobot.log.debug('Cogs downloaded.')
        else:
            yobot.log.debug('Cogs not downloaded.')
    except Exception as e:
        yobot.log.error(f'Error downloading cogs: {e}')


def remove_cogs(yobot: 'YoBot', cogs_dir: str) -> None:
    """
    Uninstalls Cogs from the terminal. Use at the user's discretion. Has ignore list.

    Args:
        yobot (YoBot): The YoBot instance.
        cogs_dir (str): The directory to download the cogs to.    
    """
    yobot.log.debug(f"Ignored cogs: {yobot.cogs_removal_blacklist}")

    try:
        remove_cogs = get_boolean_input(
            yobot, 'Do you want to uninstall cogs? (y/n) ')
        successful = False

        if remove_cogs == True:
            remove_all = get_boolean_input(
                yobot, 'Do you want to uninstall all cogs at once? (y/n) ')

            if remove_all == True:
                confirm_remove_all = get_boolean_input(
                    yobot, 'Are you sure you want to uninstall all cogs? (y/n) ')

                if confirm_remove_all == True:
                    yobot.log.info('Uninstalling all cogs...')

                    for file in os.listdir(cogs_dir):
                        if file.endswith('cog.py') and file not in yobot.cogs_removal_blacklist:
                            try:
                                os.remove(f'{cogs_dir}/{file}')
                                yobot.log.debug(
                                    f"Removed {file} from {cogs_dir}")
                            except Exception as e:
                                yobot.log.error(
                                    f"Error occurred while removing {file}: {e}")
                else:
                    yobot.log.info('Cogs not uninstalled.')
            else:
                yobot.log.info(
                    'Fetching the list of cogs from the cogs directory...')
                files = [file for file in os.listdir(cogs_dir) if file.endswith(
                    'cog.py') and file not in yobot.cogs_removal_blacklist]
                yobot.log.debug(f"List of installed cogs: {files}")

                for i, file in enumerate(files, start=1):
                    yobot.log.info(f'{i}. {file}')

                selected_cogs = input(
                    'Enter the numbers of the cogs you want to uninstall (separated by commas): ')
                selected_cogs = [int(num.strip())
                                 for num in selected_cogs.split(',')]
                confirm_removal = get_boolean_input(
                    yobot, 'Are you sure you want to uninstall the selected cogs? (y/n) ')

                if confirm_removal == True:
                    successful = True
                    yobot.log.info('Uninstalling selected cogs...')

                    for cog_index in selected_cogs:
                        cog_name = files[cog_index - 1]
                        try:
                            os.remove(f'{cogs_dir}/{cog_name}')
                            yobot.log.debug(
                                f"Removed {cog_name} from {cogs_dir}")
                            yobot.log.info(f'{cog_name} uninstalled.')
                        except Exception as e:
                            yobot.log.error(
                                f"Error occurred while removing {cog_name}: {e}")

                    if successful == True:
                        yobot.log.info('Cogs uninstalled.')

                    list_cogs(yobot, cogs_dir)
                else:
                    yobot.log.info('Cogs not uninstalled.')
    except Exception as e:
        yobot.log.error(f"Error occurred while uninstalling cogs: {e}")


def list_cogs(yobot: 'YoBot', cogs_dir: str) -> list:
    """
    Lists installed cogs from the terminal. Use at the user's discretion.

    Args:
        yobot (YoBot): The YoBot instance.
        cogs_dir (str): The directory to download the cogs to.

    Returns:
        list: A list of the installed cogs.
    """
    try:
        yobot.log.debug(
            f"Fetching list of installed cogs from directory '{cogs_dir}'...")
        files = [file for file in os.listdir(
            cogs_dir) if file.endswith('cog.py')]

        if not files:
            yobot.log.info('No cogs installed.')
            return []
        else:
            yobot.log.info('List of installed cogs:')

            for i, file in enumerate(files, start=1):
                yobot.log.info(f'{i}. {file}')
            yobot.log.debug(
                f"List of installed cogs fetched successfully from directory '{cogs_dir}'.")
            return files
    except FileNotFoundError:
        yobot.log.error(f"The directory '{cogs_dir}' does not exist.")
        return []
    except Exception as e:
        yobot.log.error(
            f"An error occurred while fetching the list of installed cogs: {e}")
        return []


def load_public_cog_key(yobot: 'YoBot', public_key_file: str) -> Union[RSAPublicKey, None]:
    """
    Loads the public key from the public key file.

    Args:
        yobot (YoBot): The YoBot instance.
        public_key_file (str): The public key file.
    Returns:
        public_key: (): The public key object.
    """
    try:
        yobot.log.debug(f"Loading public key from file '{public_key_file}'...")
        with open(public_key_file, 'rb') as file:
            public_key = load_pem_public_key(
                file.read(),
                backend=default_backend()
            )
            if not isinstance(public_key, RSAPublicKey):
                yobot.log.error(
                    f"The public key in the file '{public_key_file}' is not an RSA key.")
                return None

        yobot.log.debug(
            f"Public key loaded successfully from file '{public_key_file}'.")
        return public_key
    except FileNotFoundError:
        yobot.log.error(
            f"The public key file '{public_key_file}' does not exist.")
        return None

    except Exception as e:
        yobot.log.error(
            f"An error occurred while loading the public key from file '{public_key_file}': {e}")
        return None


def verify_cog_signature(yobot: 'YoBot', cog_file: str, signature_file: str, public_key) -> bool:
    """
    Verifies the signature of a cog using the public key and the signature file.

    Args:
        yobot (YoBot): The YoBot instance.
        cog_file (str): The cog file.
        signature_file (str): The signature file.
        public_key (rsa.RSAPublicKey): The public key.
    """
    try:
        with open(cog_file, 'rb') as file:
            cog_data = file.read()
    except FileNotFoundError:
        yobot.log.error(f"The cog file '{cog_file}' does not exist.")
        yobot.log.debug(
            f"YoBot attempted to read the cog file at '{cog_file}' but could not find it.")
        return False

    cog_hash = hashlib.sha256(cog_data).digest()

    try:
        with open(signature_file, 'rb') as file:
            signature = file.read()
    except FileNotFoundError:
        yobot.log.error(
            f"The signature file '{signature_file}' does not exist.")
        yobot.log.debug(
            f"YoBot attempted to read the signature file at '{signature_file}' but could not find it.")
        return False

    try:
        public_key.verify(
            signature,
            cog_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        yobot.log.debug(
            f"The signature is valid for the cog file '{cog_file}'.")
        return True
    except ValueError as e:
        yobot.log.error(
            f"The signature is invalid for the cog file '{cog_file}'.")
        yobot.log.debug(
            f"YoBot attempted to verify the signature of '{cog_file}' but encountered an error: {str(e)}")
        return False


def verify_all_cogs(yobot: 'YoBot', cogs_dir: str, public_key_file: str, cog_blacklist: list[str] = []) -> bool:
    """
    Verifies all installed cogs from the terminal.

    Args:
        yobot (YoBot): The YoBot instance.
        cogs_dir (str): The directory of the cogs.
        public_key_file (str): The public key file.
        cog_blacklist (List[str]): A list of cogs to skip verification on.
    """
    try:
        yobot.log.info('Verifying all cogs...')
        config = load_config(yobot.config_file)

        cogs = list_cogs(yobot, cogs_dir)
        sigs_dir = os.path.join(cogs_dir, 'sigs')
        public_key = load_public_cog_key(yobot, public_key_file)

        if not cogs:
            yobot.log.info('No cogs to verify.')
            return False

        all_cogs_valid = True

        for cog in cogs:
            if cog in cog_blacklist:
                yobot.log.warning(f"Blacklisted: {cog} Skipped check.")
                continue

            cog_path = os.path.join(cogs_dir, cog)
            signature_path = os.path.join(sigs_dir, f"{cog}.sig")

            if not os.path.exists(signature_path):
                yobot.log.error(f"No signature found for {cog}.")
                yobot.log.debug(
                    f"Expected signature at {signature_path} for cog at {cog_path}.")
                all_cogs_valid = False
                continue

            is_valid = verify_cog_signature(
                yobot, cog_path, signature_path, public_key)

            if is_valid:
                yobot.log.info(f"{cog} signature is valid.")
            else:
                yobot.log.error(f"{cog} signature is NOT valid.")
                yobot.log.debug(
                    f"Signature at {signature_path} is not valid for cog at {cog_path}.")
                all_cogs_valid = False

        if not all_cogs_valid:
            yobot.log.debug(
                f"YoBot has encountered a fatal error during cog verification.")
        else:
            yobot.log.debug(f"All cogs are valid.")

        return all_cogs_valid
    except Exception as e:
        yobot.log.error(f"An error occurred during cog verification: {e}")
        return False


def toggle_debug_mode(yobot: 'YoBot') -> None:
    """
    Toggles debug log messages.
    """
    try:
        config = load_config(yobot.config_file)
        if config['log_level'] == 'DEBUG':
            yobot.log.info('Disabling debug mode...')
            update_config(yobot.config_file, {"log_level": "INFO"})
            yobot.log.info('Restarting to apply changes...')
        else:
            yobot.log.info('Enabling debug mode...')
            update_config(yobot.config_file, {"log_level": "DEBUG"})
            yobot.log.setLevel(logging.DEBUG)
            yobot.log.info('Restarting to apply changes...')
        input('Press ENTER to EXIT.')
        yobot.stop_bot()
    except FileNotFoundError:
        yobot.log.warning(f"Config file {yobot.config_file} not found.")
    except yaml.YAMLError as e:
        yobot.log.warning(
            f"Error loading config file {yobot.config_file}: {e}")
    except Exception as e:
        yobot.log.warning(f"An error occurred while toggling debug mode: {e}")
    else:
        yobot.log.debug('Debug mode toggled successfully.')


def toggle_dev_mode(yobot: 'YoBot') -> None:
    """
    Toggles dev mode.

    Args:
        yobot (YoBot): The YoBot instance.
    """
    try:
        config = load_config(yobot.config_file)
        if config['dev_mode'] == True:
            yobot.log.info('Disabling dev mode...')
            update_config(yobot.config_file, {"dev_mode": False})
            yobot.log.info('Restarting to apply changes...')
        else:
            yobot.log.info('Enabling dev mode...')
            update_config(yobot.config_file, {"dev_mode": True})
            yobot.log.info('Restarting to apply changes...')
        input('Press ENTER to EXIT.')
        yobot.stop_bot()
    except FileNotFoundError:
        yobot.log.warning(f"Config file {yobot.config_file} not found.")
    except yaml.YAMLError as e:
        yobot.log.warning(
            f"Error loading config file {yobot.config_file}: {e}")
    except Exception as e:
        yobot.log.warning(f"An error occurred while toggling dev mode: {e}")
    else:
        yobot.log.debug('Dev mode toggled successfully.')


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


def add_blacklist(yobot: 'YoBot') -> None:
    """
    Add something to a blacklist.
    """
    edit_confirm = get_boolean_input(
        yobot, 'Are you sure you want to add to the blacklist? (y/n) ')

    if not edit_confirm:
        return
    else:
        yobot.log.info('Which blacklist would you like to add to?')
        yobot.log.info('1. Cog Removal Blacklist')
        yobot.log.info('2. Cog Verification Blacklist')

        blacklist_choice = input('Choice: ')

        config = load_config(yobot.config_file)

        if blacklist_choice == '1':
            cogs = list_cogs(yobot, yobot.cogs_dir)

            yobot.log.info('Choose the cog to add to the blacklist:')
            for i, cog in enumerate(cogs, start=1):
                yobot.log.info(f"{i}. {cog}")

            cog_index = int(
                input('Enter the number of the cog you want to blacklist: '))
            cog_name = cogs[cog_index - 1]

            blacklist = config.get('blacklist', {}).get('cog_removal', [])

            if cog_name in blacklist:
                yobot.log.warning(
                    f"'{cog_name}' is already in the cog removal blacklist.")
                return

            blacklist.append(cog_name)

            updated_config = {"blacklist": {'cog_removal': blacklist}}

            try:
                update_config(yobot.config_file, updated_config)
            except Exception as e:
                yobot.log.debug(
                    f"Failed to update the configuration file: {e}")
                return yobot.log.warning('Failed to add the cog to the cog removal blacklist.')

            yobot.log.info(
                f"'{cog_name}' has been added to the cog removal blacklist.")

        elif blacklist_choice == '2':
            cog_name = input(
                'Enter the name of the cog you would like to add: ')

            blacklist = config.get('blacklist', {}).get('cog_verify', [])

            if cog_name in blacklist:
                yobot.log.warning(
                    f"'{cog_name}' is already in the cog verification blacklist.")
                return

            blacklist.append(cog_name)

            updated_config = {"blacklist": {'cog_verify': blacklist}}

            try:
                update_config(yobot.config_file, updated_config)
            except Exception as e:
                yobot.log.debug(
                    f"Failed to update the configuration file: {e}")
                return yobot.log.warning('Failed to add the cog to the cog verification blacklist.')

            yobot.log.info(
                f"'{cog_name}' has been added to the cog verification blacklist.")

        else:
            yobot.log.info(f"'{blacklist_choice}' is not a valid choice.")
            return yobot.log.warning('Blacklist edit aborted.')


def remove_blacklist(yobot: 'YoBot') -> None:
    """
    Remove something from a blacklist.
    """
    try:
        edit_confirm = get_boolean_input(
            yobot, 'Are you sure you want to remove from the blacklist? (y/n) ')

        if not edit_confirm:
            return
        else:
            yobot.log.info('Which blacklist would you like to remove from?')
            yobot.log.info('1. Cog Removal Blacklist')
            yobot.log.info('2. Cog Verification Blacklist')

            blacklist_choice = input('Choice: ')

            # Load existing configuration
            config = load_config(yobot.config_file)
            blacklist = config.get('blacklist', {})

            if blacklist_choice == '1':
                blacklist_cog_removal = blacklist.get('cog_removal', [])

                if not blacklist_cog_removal:
                    yobot.log.warning('Cog removal blacklist is empty.')
                    return

                yobot.log.info(
                    'Here are the current cogs in the cog removal blacklist:')
                for i, cog in enumerate(blacklist_cog_removal):
                    yobot.log.info(f'{i+1}. {cog}')
                cog_number = int(
                    input('Enter the number of the cog you would like to remove: '))

                if cog_number < 1 or cog_number > len(blacklist_cog_removal):
                    yobot.log.warning('Invalid cog number.')
                    return

                cog_name = blacklist_cog_removal.pop(cog_number - 1)
                blacklist['cog_removal'] = blacklist_cog_removal

            elif blacklist_choice == '2':
                blacklist_cog_verify = blacklist.get('cog_verify', [])

                if not blacklist_cog_verify:
                    yobot.log.warning('Cog verification blacklist is empty.')
                    return

                yobot.log.info(
                    'Here are the current cogs in the cog verify blacklist:')
                for i, cog in enumerate(blacklist_cog_verify):
                    yobot.log.info(f'{i+1}. {cog}')
                cog_number = int(
                    input('Enter the number of the cog you would like to remove: '))

                if cog_number < 1 or cog_number > len(blacklist_cog_verify):
                    yobot.log.warning('Invalid cog number.')
                    return

                cog_name = blacklist_cog_verify.pop(cog_number - 1)
                blacklist['cog_verify'] = blacklist_cog_verify

            else:
                yobot.log.warning(
                    f"'{blacklist_choice}' is not a valid choice.")
                return yobot.log.warning('Blacklist edit aborted.')

            if cog_name in blacklist.get('cog_removal', []) or cog_name in blacklist.get('cog_verify', []):
                yobot.log.warning(f"'{cog_name}' is already in the blacklist.")
                return

            update_config(yobot.config_file, {"blacklist": blacklist})
            yobot.log.info(
                f"'{cog_name}' has been removed from the chosen blacklist.")

    except Exception as e:
        yobot.log.debug(f"Error removing from blacklist: {e}")
        