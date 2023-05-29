import discord
import json


async def update_yobot(yobot):
    """Updates YoBot's name, presence, and avatar to config values on Discord servers."""
    config_file = yobot.config_file
    successful = True # Whether or not the update was successful.
    yobot.log.info('Checking for updates to YoBot settings...')
    if yobot.config['update_bot'] == True:
        yobot.log.info('First run or changes detected!')
        yobot.log.info('Setting name, presence, and avatar to config values.')
        yobot.log.warning('This action is rate limited, so to change it later, edit the config file.')
        yobot.log.warning('You may also manually set these attributes with the terminal.')
        try:
            await yobot.user.edit(username=yobot.bot_name, avatar=yobot.avatar) # Try to change the name and avatar on Discord servers.
            await yobot.change_presence(activity=discord.Game(name=yobot.presence)) # Try to change the presence on Discord servers.
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
                
    
async def welcome_to_yobot(yobot):
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
        
        
def exit_bot_terminal(yobot):
    """Shutsdown YoBot from the terminal."""
    yobot.stop_bot()


async def set_bot_name(yobot):
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
            await yobot.user.edit(username=new_name) # Try to change the name on Discord servers.
            yobot.log.info('Config change, bot_name: {} -> {}'.format(yobot.config['bot_name'], new_name))
        except Exception as e:
            yobot.log.error('Error: {}'.format(e))
            yobot.log.warning('Bot name not changed on Discord servers.')
    else:
        yobot.log.info('Name not changed.')


async def set_bot_avatar(yobot):
    """
    Changes YoBot's avatar from the terminal.
    
    This updates the config file and Discord servers.
    """
    yobot.log.info('This sets the avatar to the image at ../resources/images/avatar.png')
    change_avatar = get_boolean_input(yobot, 'Do you want to change the avatar? (y/n) ')
    successful = True
    config = yobot.config
    if change_avatar == True:
        try:
            await yobot.user.edit(avatar=yobot.avatar) # Try to change the avatar on Discord servers.
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


async def set_bot_presence(yobot):
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


async def sync_commands(yobot):
    """Synchronizes YoBot's commands from the terminal."""
    synchronize = get_boolean_input(yobot, 'Do you want to synchronize commands? (y/n) ')
    if synchronize == True:
        sync_list = await yobot.tree.sync()  # Try to update commands on Discord servers.
        yobot.log.info(f'{len(sync_list)} commands synchronized.')
    else:
        yobot.log.info('Commands not synchronized.')
        
        
async def set_owner(yobot):
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


def ping(yobot):
    """Pong!"""
    yobot.log.info('Pong!')


def show_help(yobot):
    """Shows the help menu."""
    black = '\033[30m'
    cyan = '\033[36m'
    green = '\033[32m'
    purple = '\033[35m'
    bold = '\033[1m'
    reset = '\033[0m'
    yobot.log.info(f"{black}{'-' * 20}[ {purple}{bold}Available commands{reset}{black} ]{'-' * 20}{reset}")
    yobot.log.info('')
    yobot.log.info(f"{cyan}Simply type the command you want to execute and press enter.{reset}")
    yobot.log.info(f"{cyan}A brief description of the command will be displayed below.{reset}")
    yobot.log.info('')
    yobot.log.info(f"{green}setbotname{' ' * 12}{black}- Changes the current YoBot name.{reset}")
    yobot.log.info(f"{green}setavatar{' ' * 13}{black}- Changes the current YoBot avatar.{reset}")
    yobot.log.info(f"{green}setstatus{' ' * 13}{black}- Changes the current YoBot status.{reset}")
    yobot.log.info(f"{green}synccommands{' ' * 10}{black}- Synchronizes commands with Discord.{reset}")
    yobot.log.info(f"{green}exit{' ' * 18}{black}- Shuts YoBot and the script down.{reset}")
    yobot.log.info(f"{green}ping{' ' * 18}{black}- Pongs.{reset}")
    yobot.log.info(f"{green}help{' ' * 18}{black}- Displays this message.{reset}")
    yobot.log.info('')
    yobot.log.info(f"{black}{'-' * 18}[ {purple}{bold}End available commands{reset}{black} ]{'-' * 18}{reset}")
    
    
def get_boolean_input(yobot, prompt: str):
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