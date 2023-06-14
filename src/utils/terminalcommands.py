import logging
import os
import traceback
from typing import TYPE_CHECKING

import discord
import yaml

from utils.yobotlib import (get_boolean_input, download_cogs, load_config, update_config)

if TYPE_CHECKING:
    from bot.yobot import YoBot


class YoBotTerminalCommands():
    """
    This class handles YoBotLogger terminal commands.
    These commands are meant to be uni-directional. 

    Args:
        yobot (Yobot): The Yobot instance.
        terminal_command (str): The terminal command.
    """

    def __init__(self: 'YoBotTerminalCommands', yobot: 'YoBot', terminal_command: str):
        self.yobot = yobot
        self.cog_repo_owner = self.yobot.repo_info['repo_owner']
        self.cog_repo_name = self.yobot.repo_info['repo_name']
        self.cog_repo_info = self.yobot.repo_info['repo_info']
        self.terminal_command = terminal_command

    async def handle_terminal_command(self):
        """
        Handles the terminal command.

        Do not call these from outside sources.

        Terminal -> External Application == GOOD!

        External Application -> Terminal == BAD!
        """
        user_command = self.terminal_command.lower()
        self.yobot.log.info('Received command: {}'.format(user_command))

        if user_command in ['exit', 'quit', 'shutdown']:
            self.yobot.log.debug('Exiting bot terminal...')
            exit_bot_terminal(self.yobot)

        elif user_command in ['help', 'h', '?']:
            self.yobot.log.debug('Showing help...')
            show_help(self.yobot)

        elif user_command in ['ping', 'p']:
            self.yobot.log.debug('Pinging...')
            ping(self.yobot)

        elif user_command in ['setbotname', 'setbot', 'sbn']:
            self.yobot.log.debug('Setting bot name...')
            await set_bot_name(self.yobot)

        elif user_command in ['setpresence', 'setpres', 'sp']:
            self.yobot.log.debug('Setting bot presence...')
            await set_bot_presence(self.yobot)

        elif user_command in ['setavatar', 'setava', 'sa']:
            self.yobot.log.debug('Setting bot avatar...')
            await set_bot_avatar(self.yobot)

        elif user_command in ['setowner', 'setown']:
            self.yobot.log.debug('Setting owner...')
            await set_owner(self.yobot)

        elif user_command in ['reload', 'sync', 'r']:
            self.yobot.log.debug('Syncing commands...')
            await sync_commands(self.yobot)

        elif user_command in ['wipebot', 'wipeconfig', 'wipe', 'wb']:
            self.yobot.log.debug('Wiping bot config...')
            wipe_config(self.yobot)

        elif user_command in ['getcog', 'getcogs', 'gc']:
            self.yobot.log.debug('Downloading cogs...')
            download_cogs(self.yobot, self.cog_repo_owner, self.cog_repo_name, self.cog_repo_info)
            await self.yobot.load_cogs()
            self.yobot.log.info('Reloaded all cogs.')
            self.yobot.log.info('You may need to resync with Discord to apply new commands.')
            await sync_commands(self.yobot)

        elif user_command in ['removecog', 'removecogs', 'rc']:
            self.yobot.log.debug('Removing cogs...')
            remove_cogs(self.yobot, self.yobot.cogs_dir)

        elif user_command in ['listcogs', 'list', 'lc']:
            self.yobot.log.debug('Listing cogs...')
            list_cogs(self.yobot, self.yobot.cogs_dir)

        elif user_command in ['alias', 'aliases', 'a']:
            self.yobot.log.debug('Showing aliases...')
            show_aliases(self.yobot)

        elif user_command in ['debug', 'd']:
            self.yobot.log.debug('Toggling debug mode...')
            toggle_debug_mode(self.yobot)

        elif user_command in ['developer', 'dev', 'devmode', 'dm']:
            self.yobot.log.debug('Toggling developer mode...')
            toggle_dev_mode(self.yobot)

        elif user_command in ['addblacklist', 'addbl', 'abl']:
            self.yobot.log.debug('Adding to blacklist...')
            add_blacklist(self.yobot)

        elif user_command in ['removeblacklist', 'rmblist', 'rmbl']:
            self.yobot.log.debug('Removing from blacklist...')
            remove_blacklist()
            
        else:
            self.yobot.log.info(
                f"'{user_command}' is not a recognized command.")



# Terminal Commands Functions

def add_blacklist(yobot: 'YoBot') -> None:
    """
    Add something to a blacklist.
    """
    try:
        edit_confirm = get_boolean_input(yobot, 'Are you sure you want to add to the blacklist? (y/n) ')
        config = load_config(yobot.config_file)
        
        if not edit_confirm:
            return
        else:
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
    except Exception as e:
        yobot.log.debug(f"Failed to add to the cog removal blacklist: {e}")
        yobot.log.warning('Failed to add to the cog removal blacklist.')


def remove_blacklist(yobot: 'YoBot') -> None:
    """
    Remove something from a blacklist.
    """
    try:
        edit_confirm = get_boolean_input(yobot, 'Are you sure you want to remove from the blacklist? (y/n) ')

        if not edit_confirm:
            return
        else:

            config = load_config(yobot.config_file)
            blacklist = config.get('blacklist', {})
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

        update_config(yobot.config_file, {"blacklist": blacklist})
        yobot.log.info(
            f"'{cog_name}' has been removed from the chosen blacklist.")

    except Exception as e:
        yobot.log.debug(f"Error removing from blacklist: {e}")
        yobot.log.warning('Failed to remove from blacklist.')
    
    
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
                yobot.log.warning('It will automatically be changed on the next startup.')
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
    yobot.log.debug('Synchronizing commands...')
    try:
        synchronize = get_boolean_input(
            yobot, 'Do you want to synchronize commands? (y/n) ')

        if synchronize == True:
            # Try to update commands on Discord servers.
            yobot.log.debug('Updating commands on Discord servers...')
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


def show_help(yobot: 'YoBot') -> None:
    """
    Shows the help menu.

    Args:
        yobot (YoBot): The bot instance.
    """
    black = '\u001b[30m'
    cyan = '\u001b[36m'
    green = '\u001b[32m'
    purple = '\u001b[35m'
    bold = '\u001b[1m'
    reset = '\u001b[0m'
    commands = {
        'exit': 'Shuts YoBot and the script down.',
        'help': 'Displays this message.',
        'ping': 'Pongs.',
        'setbotname': 'Changes the current YoBot name.',
        'setpresence': 'Changes the current YoBot presence.',
        'setavatar': 'Changes the current YoBot avatar.',
        'setowner': 'Sets the owner of the bot.',
        'reload': 'Synchronizes commands with Discord.',
        'wipebot': 'Wipes the bot\'s configuration files.',
        'getcogs': 'Downloads and loads cogs.',
        'removecog': 'Removes cogs from the bot.',
        'listcogs': 'Lists all cogs currently loaded.',
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
    black = '\u001b[30m'
    purple = '\u001b[35m'
    green = '\u001b[32m'
    bold = '\u001b[1m'
    reset = '\u001b[0m'
    aliases = {
        'exit': ['quit', 'shutdown'],
        'help': ['h', '?'],
        'ping': ['p'],
        'setbotname': ['setbot', 'sbn'],
        'setpresence': ['setbotpres', 'sbp'],
        'setavatar': ['setava', 'sba'],
        'setowner': ['setown'],
        'reload': ['sync', 'r'],
        'wipebot': ['wipeconfig', 'wipe', 'wb'],
        'getcogs': ['getcogs', 'gc'],
        'removecog': ['removecogs', 'rc'],
        'listcogs': ['list', 'lc'],
        'alias': ['aliases', 'a'],
        'debug': ['d'],
        'developer': ['dev', 'devmode', 'dm'],
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
        
        
def ping(yobot: 'YoBot') -> None:
    """Pong!"""
    try:
        yobot.log.debug('Pinging...')
        yobot.log.info('Pong!')
    except Exception as e:
        yobot.log.error(f'Error in ping function: {e}')