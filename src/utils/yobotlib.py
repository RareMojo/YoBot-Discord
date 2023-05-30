import json
import os
from typing import TYPE_CHECKING

import discord
import requests

if TYPE_CHECKING:
    from bot.yobot import YoBot


def get_boolean_input(yobot: 'YoBot', prompt: str):
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
            yobot.log.warning('Invalid input. Try again.')


async def update_yobot(yobot: 'YoBot'):
    """Updates YoBot's name, presence, and avatar to config values on Discord servers."""
    config_file = yobot.config_file
    successful = True # Whether or not the update was successful.
    yobot.log.info('Checking for updates to YoBot settings...')
    
    if yobot.config['update_bot'] == True:
        yobot.log.info('First run or changes detected!')
        yobot.log.info('Setting name, presence, and avatar to config values.')
        yobot.log.warning('This action is rate limited, so to change it later, edit the config file.')
        yobot.log.warning('You may also manually set these attributes with the terminal.')
        
        try: # Try to update the bot's name, presence, and avatar on the Discord servers.
            with open(yobot.avatar, 'rb') as f:
                new_avatar = f.read() 
                await yobot.user.edit(avatar=new_avatar) # type: ignore
            await yobot.user.edit(username=yobot.config['bot_name']) # type: ignore
            await yobot.change_presence(activity=discord.Game(name=yobot.presence))
        except Exception as e:
            yobot.log.error('Error: {}'.format(e))
            yobot.log.warning('Bot name, avatar, or presence not changed on Discord servers.')
            yobot.log.warning('This will be run again on next startup.')
            successful = False
 
        if successful == True:
            yobot.log.info('Successfully synchronized YoBot settings with Discord.')
            yobot.config['update_bot'] = False
            with open(config_file, 'w') as f: # Update the config file.
                json.dump(yobot.config, f, indent=4)
    else:
        yobot.log.info('YoBot settings are up to date.')
        yobot.log.info('Connected to Discord.')
                
    
async def welcome_to_yobot(yobot: 'YoBot'):
    """Prints a welcome message to the terminal."""
    yobot.log.info('YoBot Instance Details:')
    yobot.log.info('Display name: {}'.format(yobot.bot_name)) # Print YoBot's current display name.
    yobot.log.info('Presence: {}'.format(yobot.presence)) # Print YoBot's current presence.
    
    for guild in yobot.guilds: # Print the guilds YoBot is connected to.
        yobot.log.info(f'Linked with {guild} | ID: {guild.id}')
        
    yobot.log.info('YoBot is online and ready.')
    if not yobot.config['update_bot']: # If this is not the first run, print a welcome back message.
        yobot.log.info('Welcome back to YoBot, {}!'.format(yobot.config['owner_name']))
        yobot.log.info('Type "help" for a list of terminal commands.')
        
    else: # If this is the first run, print a welcome message.
        yobot.log.info('Welcome to YoBot, {}!'.format(yobot.config['owner_name']))
        yobot.log.info('Type "help" for a list of terminal commands.')
        
        
def exit_bot_terminal(yobot: 'YoBot'):
    """Shutsdown YoBot from the terminal."""
    yobot.stop_bot()


async def set_bot_name(yobot: 'YoBot'):
    """
    Changes YoBot's name from the terminal.
    
    This updates the config file and Discord servers.
    """
    yobot.log.info(f'Current name: {yobot.config["bot_name"]}')
    change_bot_name = get_boolean_input(yobot, 'Do you want to change YoBots name? (y/n) ')
    config = yobot.config
    
    if change_bot_name == True:
        new_name = input('Enter new bot name: ')
        config['bot_name'] = new_name
        config['update_bot'] = True
        with open(yobot.config_file, 'w') as f: # Update the config file.
            json.dump(config, f, indent=4)
        try:
            await yobot.user.edit(username=new_name) # type: ignore
            yobot.log.info('Config change, bot_name: {} -> {}'.format(yobot.config['bot_name'], new_name))
        except Exception as e:
            yobot.log.error('Error: {}'.format(e))
            yobot.log.warning('Bot name not changed on Discord servers.')
    else:
        yobot.log.info('Name not changed.')


async def set_bot_avatar(yobot: 'YoBot'):
    """
    Changes YoBot's avatar from the terminal.
    
    This updates the config file and Discord servers.
    """
    yobot.log.info('This sets the avatar to the image at ../resources/images/avatar.png')
    change_avatar = get_boolean_input(yobot, 'Do you want to change the avatar? (y/n) ')
    successful = True
    config = yobot.config
    
    with open(yobot.avatar, 'rb') as f:
        new_avatar = f.read()
        
    if change_avatar == True:
        try:
            await yobot.user.edit(avatar=new_avatar) # type: ignore
        except Exception as e:
            yobot.log.error('Error: {}'.format(e))
            yobot.log.warning('Avatar not changed on Discord servers.')
            yobot.log.warning('It will automatically be changed on the next startup.')
            successful = False
            
        if successful == False:
            config['update_bot'] = True
            with open(yobot.config_file, 'w') as f: # Update the config file.
                json.dump(config, f, indent=4)
                
        if successful == True:
            yobot.log.info('Avatar changed.')
    else:
        yobot.log.info('Avatar not changed.')


async def set_bot_presence(yobot: 'YoBot'):
    """
    Changes YoBot's presence from the terminal.
    
    This updates the config file and Discord servers.
    """
    yobot.log.info('Current presence: {}'.format(yobot.presence))
    update_presence = get_boolean_input(yobot, 'Do you want to change the presence? (y/n) ')
    config = yobot.config
    
    if update_presence == True:
        new_presence = input('Enter new presence: ')
        config['presence'] = new_presence
        config['update_bot'] = True
        
        with open(yobot.config_file, 'w') as f: # Update the config file.
            json.dump(config, f, indent=4)
        try:
            await yobot.change_presence(activity=discord.Game(name=new_presence)) # Try to change the presence on Discord servers.
            yobot.log.info('Config change, presence: {} -> {}'.format(yobot.presence, new_presence))
        except Exception as e:
            yobot.log.error('Error: {}'.format(e))
            yobot.log.warning('Presence not changed.')
    else:
        yobot.log.info('Presence not changed.')


async def sync_commands(yobot: 'YoBot'):
    """Synchronizes YoBot's commands from the terminal."""
    synchronize = get_boolean_input(yobot, 'Do you want to synchronize commands? (y/n) ')
    
    if synchronize == True:
        sync_list = await yobot.tree.sync()  # Try to update commands on Discord servers.
        yobot.log.info(f'{len(sync_list)} commands synchronized.')
    else:
        yobot.log.info('Commands not synchronized.')
        
        
async def set_owner(yobot: 'YoBot'):
    """
    Changes YoBot's owner from the terminal.
    
    This updates the config file and the respected admin of YoBot.
    """
    yobot.log.info(f'Current owner: {yobot.config["owner_name"]} - {yobot.config["owner_id"]}')
    change_owner_name = get_boolean_input(yobot, 'Do you want to change YoBots owner? (y/n) ')
    config = yobot.config
    
    if change_owner_name == True:
        new_owner_name = input('Enter new owner name: ')
        new_owner_id = input('Enter new owner id: ')
        config['owner_name'] = new_owner_name
        config['owner_id'] = new_owner_id
        
        with open(yobot.config_file, 'w') as f: # Update the config file.
            json.dump(config, f, indent=4)
            
        yobot.log.info('Config change, owner_name: {} -> {}'.format(yobot.config['owner'], new_owner_name))
        yobot.log.info('Config change, owner_id: {} -> {}'.format(yobot.config['owner_id'], new_owner_id))
    else:
        yobot.log.info('Owner not changed.')
    
    
def ping(yobot: 'YoBot'):
    """Pong!"""
    yobot.log.info('Pong!')

         
def show_help(yobot: 'YoBot'):
    """Shows the help menu."""
    black = '\033[30m'
    cyan = '\033[36m'
    green = '\033[32m'
    purple = '\033[35m'
    bold = '\033[1m'
    reset = '\033[0m'
    commands = {
        'exit, shutdown': 'Shuts YoBot and the script down.',
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
        'listaliases': 'Lists all command aliases.'
    }
    
    yobot.log.info(f"{black}{'-' * 24}[ {purple}{bold}Available commands{reset}{black} ]{'-' * 24}{reset}")
    yobot.log.info('')
    yobot.log.info(f"{cyan}Simply type the command you want to execute and press enter.{reset}")
    yobot.log.info(f"{cyan}A brief description of the command will be displayed below.{reset}")
    yobot.log.info('')
    
    for command, description in commands.items():
        yobot.log.info(f"{green}{command}{' ' * (30 - len(command))}{black}- {description}{' ' * (45 - len(description))}{reset}")
    yobot.log.info('')
    yobot.log.info(f"{black}{'-' * 22}[ {purple}{bold}End available commands{reset}{black} ]{'-' * 22}{reset}")
    
    
def show_aliases(yobot: 'YoBot'):
    """Shows the aliases for YoBot's commands."""
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
        'alias': ['aliases', 'a']
    }
    
    yobot.log.info(f"{black}{'-' * 24}[ {purple}{bold}Command Aliases{reset}{black} ]{'-' * 24}{reset}")
    yobot.log.info('')
    
    for command, alias_list in aliases.items():
        aliases_str = ', '.join(alias_list)
        yobot.log.info(f"{green}{command}{' ' * (30 - len(command))}{black}- {aliases_str}{' ' * (45 - len(aliases_str))}{reset}")
    yobot.log.info('')
    yobot.log.info(f"{black}{'-' * 22}[ {purple}{bold}End command aliases{reset}{black} ]{'-' * 22}{reset}")
    

def wipe_config(yobot: 'YoBot'):
    """Wipes the config file and shuts down YoBot, causing setup to run on next startup"""
    yobot.log.warning('This will wipe the config file and shut down YoBot.')
    wipe = get_boolean_input(yobot, 'Do you want to wipe the config file? (y/n) ')
    
    if wipe == True:
        wipe_confirm = get_boolean_input(yobot, 'Are you sure you want to wipe config and restart? (y/n) ')
        
        if wipe_confirm == True:
            os.remove(yobot.config_file)
            yobot.log.info('Config file wiped.')
            yobot.log.warning('YoBot will now shut down.')
            exit_bot_terminal(yobot)
        else:
            yobot.log.info('Config file not wiped.')


def github_repo_fetch(owner: str, repo: str, repo_dir: str):
    """Fetches the list of cogs from a YoBot-related repository on GitHub."""
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{repo_dir}"
        response = requests.get(url)

        if response.status_code == 200:
            files = [file["name"] for file in response.json() if file["type"] == "file"]
            return files
        else:
            return []
    except Exception as e:
        return []


def github_repo_pull(yobot: 'YoBot', owner: str, repo: str, repo_dir: str, target_dir: str):
    """Pulls a repo from GitHub."""
    try:
        files = github_repo_fetch(owner, repo, repo_dir)

        if files:
            for file in files:
                url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/{repo_dir}/{file}"
                response = requests.get(url)

                if response.status_code == 200:
                    with open(f"{target_dir}/{file}", "wb") as f:
                        f.write(response.content)
                    yobot.log.info(f'{file} downloaded.')
                else:
                    yobot.log.error(f'Error downloading {file}.')
        else:
            yobot.log.error('Failed to retrieve the list of cogs from the repository.')
    except Exception as e:
        yobot.log.error(f'Error downloading cogs: {e}')


def download_cogs(yobot: 'YoBot', cogs_dir: str):
    """Downloads cogs from the terminal. Use for setup or at the user's discretion."""
    get_cogs = input('Do you want to download cogs? (y/n) ')
    successful = False
    if get_cogs.lower() == 'y':
        get_all_cogs = input('Do you want to download all cogs at once? (y/n) ')
        if get_all_cogs.lower() == 'y':
            yobot.log.info('Downloading all cogs from the repository...')
            github_repo_pull(yobot, "RareMojo", "YoBot-Discord-Cogs", "Cogs", cogs_dir)
        else:
            yobot.log.info('Fetching the list of cogs from the repository...')
            files = github_repo_fetch("RareMojo", "YoBot-Discord-Cogs", "Cogs")

            if files:
                yobot.log.info('List of cogs available:')
                for i, file in enumerate(files, start=1):
                    yobot.log.info(f'{i}. {file}')

                selected_cogs = input('Enter the numbers of the cogs you want to download (separated by commas): ')
                selected_cogs = [int(num.strip()) for num in selected_cogs.split(',')]

                successful = True
                yobot.log.info('Downloading selected cogs from the repository...')
                for cog_index in selected_cogs:
                    cog_name = files[cog_index - 1]
                    url = f"https://raw.githubusercontent.com/RareMojo/YoBot-Discord-Cogs/master/Cogs/{cog_name}"
                    response = requests.get(url)

                    if response.status_code == 200:
                        with open(f"{cogs_dir}/{cog_name}", "wb") as f:
                            f.write(response.content)
                        yobot.log.info(f'{cog_name} downloaded.')
                    else:
                        yobot.log.error(f'Error downloading {cog_name}.')

                # List installed cogs after downloading
                list_cogs(yobot, cogs_dir)
            else:
                yobot.log.error('Failed to retrieve the list of cogs from the repository.')

            if successful:
                yobot.log.info('Cogs downloaded.')
    else:
        yobot.log.info('Cogs not downloaded.')


def remove_cogs(yobot: 'YoBot', cogs_dir: str):
    """Uninstalls Cogs from the terminal. Use at the user's discretion. Has ignore list."""
    ignored_cogs = ['discordeventscog.py', 'yobotcommandscog.py']  # example ignored cogs
    remove_cogs = get_boolean_input(yobot, 'Do you want to uninstall cogs? (y/n) ')
    successful = False
    
    if remove_cogs == True:
        remove_all = get_boolean_input(yobot, 'Do you want to uninstall all cogs at once? (y/n) ')
        
        if remove_all == True:
            confirm_remove_all = get_boolean_input(yobot, 'Are you sure you want to uninstall all cogs? (y/n) ')
            
            if confirm_remove_all == True:
                    yobot.log.info('Uninstalling all cogs...')
                    
                    for file in os.listdir(cogs_dir):
                        if file.endswith('cog.py') and file not in ignored_cogs:
                            os.remove(f'{cogs_dir}/{file}')
            else:
                yobot.log.info('Cogs not uninstalled.')               
        else:
            yobot.log.info('Fetching the list of cogs from the cogs directory...')
            files = [file for file in os.listdir(cogs_dir) if file.endswith('cog.py') and file not in ignored_cogs]
            
            for i, file in enumerate(files, start=1):
                yobot.log.info(f'{i}. {file}')

            selected_cogs = input('Enter the numbers of the cogs you want to uninstall (separated by commas): ')
            selected_cogs = [int(num.strip()) for num in selected_cogs.split(',')]
            confirm_removal = get_boolean_input(yobot, 'Are you sure you want to uninstall the selected cogs? (y/n) ')
            
            if confirm_removal == True:
                successful = True
                yobot.log.info('Uninstalling selected cogs...')
                
                for cog_index in selected_cogs:
                    cog_name = files[cog_index - 1]
                    os.remove(f'{cogs_dir}/{cog_name}')
                    yobot.log.info(f'{cog_name} uninstalled.')
                    
                if successful == True:
                    yobot.log.info('Cogs uninstalled.')
                    
                # List installed cogs after uninstalling
                list_cogs(yobot, cogs_dir)
            else:
                yobot.log.info('Cogs not uninstalled.')
                
                
def list_cogs(yobot: 'YoBot', cogs_dir: str):
    """Lists installed cogs from the terminal. Use at the user's discretion."""
    list_cogs = get_boolean_input(yobot, 'Do you want to list installed cogs? (y/n) ')
    
    if list_cogs == True:
        yobot.log.info('Fetching the list of cogs from the cogs directory...')
        files = [file for file in os.listdir(cogs_dir) if file.endswith('cog.py')]
        
        for i, file in enumerate(files, start=1):
            yobot.log.info(f'{i}. {file}')
        yobot.log.info('Installed cogs listed.')
    else:
        yobot.log.info('Cogs not listed.')