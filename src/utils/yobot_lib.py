import csv
import os
import shutil
import subprocess
import tempfile
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
        if yobot.config_file.get('update_bot') == False:
            yobot.log.info('Welcome back to YoBot, {}!'.format(
                yobot.config_file.get('owner_name')))
            yobot.log.info('Type "help" for a list of terminal commands.')

        else:  # If this is the first run, print a welcome message.
            yobot.log.info('Welcome to YoBot, {}!'.format(
                yobot.config_file.get('owner_name')))
            yobot.log.info(
                'Be sure to check out the documentation at the GitHub repository.')
            yobot.log.info(
                'If you ever want to design a cog, check out the YoBot-Discord-Cog GitHub repository.')
            yobot.log.info('Type "help" for a list of terminal commands.')

    except Exception as e:
        yobot.log.error(f'Error in welcome_to_yobot function: {e}')


async def update_with_discord(yobot: 'YoBot') -> None:
    """
    Updates YoBot's name, presence, and avatar to config values on Discord servers.

    Args:
        yobot (YoBot): The bot instance.
    """
    successful = True  # Whether or not the update was successful.
    yobot.log.debug('Starting update_with_discord function...')
    yobot.log.debug('Checking for updates to YoBot settings...')
    update = yobot.config_file.get('update_bot')
    if update == True:
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
            await yobot.user.edit(username=yobot.config_file.get('bot_name'))
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
            yobot.log.debug(
                'Successfully synchronized YoBot settings with Discord.')
            yobot.config_file.load()
            yobot.config_file.set('update_bot', False)
            yobot.config_file.save()
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
            

def download_cogs(yobot: 'YoBot', owner: str, repo: str, file_name: str) -> list:
    """
    Fetches a CSV file from a GitHub repository.

    Args:
        yobot (YoBot): The YoBot instance.
        owner (str): The owner of the repo.
        repo (str): The name of the repo.
        file_name (str): The name of the file to fetch.

    Returns:
        list: The contents of the CSV file.
    """
    getcogs = get_boolean_input(yobot, 'Would you like to download extra extensions? (y/n) ')
    if getcogs == True:
        try:
            url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/{file_name}"
            response = requests.get(url)

            if response.status_code == 200:
                yobot.log.debug(f'{file_name} fetched.')
                csv_contents = response.text.splitlines()
                csv_reader = csv.reader(csv_contents)
                headers = next(csv_reader)
                rows = list(csv_reader)
                yobot.log.debug(f'Loaded file {file_name}:')
                yobot.log.info(f"{headers[0]} | {headers[1]} | {headers[2]}")
                
                for i, row in enumerate(rows):
                    yobot.log.info(f"{i+1}: {row[0]}, {row[1]} Author: {row[2]}")
                row_num = input("Enter the row number of the extension to install: ")
                try:
                    row_num = int(row_num)
                    if row_num < 1 or row_num > len(rows):
                        raise ValueError
                except ValueError:
                    yobot.log.error("Invalid row number.")
                    return []
                link = rows[row_num-1][headers.index("Repo")]
                extension_name = link.split("/")[-1]
                try:
                    yobot.log.info(f"Downloading {extension_name}...")
                    github_clone_repo(yobot, link, yobot.cogs_dir)
                except Exception as e:
                    yobot.log.error(f"Error downloading {extension_name}: {e}")
                    return []
                yobot.log.info(f"{extension_name} download successful.")
                return rows
            else:
                yobot.log.error(
                    f'Error fetching {file_name}. Status code: {response.status_code}')
                return []
        except Exception as e:
            yobot.log.error(f'Error fetching {file_name}: {e}')
            yobot.log.debug(f'Error details: {traceback.format_exc()}')
            return []
    else:
        yobot.log.info("Skipping extra extensions.")
        yobot.log.info("If you would like to install extra extensions, run the command 'getcogs'.")
            

def github_clone_repo(yobot: 'YoBot', repo: str, target_dir: str):
    """
    Clones a GitHub repository.
    
    Args:
        yobot (YoBot): The YoBot instance.
        repo (str): The GitHub repository to clone.
        target_dir (str): The directory to clone the repository to.
    """
    try:
        yobot.log.debug(f"Cloning {repo} to {target_dir}...")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            command = ['git', 'clone', repo, temp_dir]
            subprocess.check_call(command)
            
            for filename in os.listdir(temp_dir):
                if filename == '.git': 
                    continue

                src_file = os.path.join(temp_dir, filename)
                dst_file = os.path.join(target_dir, filename)

                if os.path.exists(dst_file):
                    if os.path.isfile(dst_file) or os.path.islink(dst_file):
                        os.unlink(dst_file)
                    else:
                        shutil.rmtree(dst_file)

                shutil.move(src_file, target_dir)
        
    except Exception as e:
        yobot.log.error(f"Error cloning {repo}: {e}")
        yobot.log.debug(f"Error details: {traceback.format_exc()}")
    else:
        yobot.log.debug(f"Cloned {repo} to {target_dir}.")