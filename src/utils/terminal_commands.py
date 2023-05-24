import asyncio
import os
import re

import discord

from .yobotlib import (get_boolean_input, log, set_avatar, set_display_name,
                       sync_commands, update_config_file)


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..',))
CORE_CONFIG_FILE = os.path.join(ROOT_DIR, 'configs', 'core_config.ini')
LANGUAGES_DIR = os.path.join(ROOT_DIR, 'resources', 'texts', 'system', 'languages')
LANGUAGE_EXTRAS_DIR = os.path.join(LANGUAGES_DIR, 'extras')


def set_language():
    """
    Allows the user to choose a language and returns the corresponding language file.

    Returns:
        str: The path to the selected language file.
    """
    language_files = os.listdir(LANGUAGES_DIR)
    extra_language_files = os.listdir(LANGUAGE_EXTRAS_DIR)

    lang_codes = [(re.match(r'(\w+)_', lang_file).group(1), os.path.join(LANGUAGES_DIR, lang_file)) for lang_file in language_files if re.match(r'(\w+)_', lang_file)]
    extra_lang_codes = [(re.match(r'(\w+)_', lang_file).group(1), os.path.join(LANGUAGE_EXTRAS_DIR, lang_file)) for lang_file in extra_language_files if re.match(r'(\w+)_', lang_file)]
    
    print('Available languages:')
    for i, (lang_code, _) in enumerate(lang_codes, 1):
        print(f'{i}. {lang_code[:-7]}')

    chosen_lang = int(input('Choose a language by number: '))
    if chosen_lang == 2:
        extra = get_boolean_input('Do you want to add an extra language style? (y/n) ')
        if not extra:
            current_lang = lang_codes[chosen_lang - 1][1]
        else:
            print('Available language styles:')
            for i, (lang_code, _) in enumerate(extra_lang_codes, 1):
                print(f'{i}. {lang_code[:-7]}')
            chosen_extra_lang = int(input('Choose a language style by number: '))
            current_lang = extra_lang_codes[chosen_extra_lang - 1][1]
    else:
        current_lang = lang_codes[chosen_lang - 1][1]

    return current_lang


async def terminal_command_loop(self):
    """Terminal commands listener."""
    loop = asyncio.get_running_loop()

    while self.running:
        terminal_command = await loop.run_in_executor(None, input, '>')
        await handle_terminal_command(self, terminal_command)


async def handle_terminal_command(yobot, terminal_command):
    """
    These commands are meant to be uni-directional. 

    Do not allow the Discord bot to issue these commands.

    Terminal -> External Application == GOOD!

    External Application -> Terminal == BAD!
    
    Parameters:
        yobot (instance): The yobot instance.
        terminal_command (str): The terminal command.
    """
    cmd = terminal_command.lower()

    match cmd:
        case 'exit':
            log(msg_key='terminal_callback', command=cmd)
            yobot.stop_bot()


        case 'restart':
            log(msg_key='terminal_callback', command=cmd)
            yobot.restart_bot()


        case 'help':
            log(msg_key='terminal_callback', command=cmd)
            log(msg='ADD_HELP_INFO_HERE')


        case 'language':
            log(msg_key='terminal_callback', command=cmd)
            change_language = get_boolean_input('Do you want to change the language? (y/n) ')
            if change_language:
                new_language = set_language()
                update = {'settings': {'language': new_language}}
                update_config_file(CORE_CONFIG_FILE, update)


        case 'ping':
            log(msg_key='terminal_callback', command=cmd)
            log(msg='Pong!')


        case 'sync':
            log(msg_key='terminal_callback', command=cmd)
            synchronize = get_boolean_input('Do you want to synchronize commands? (y/n) ')
            if synchronize:
                log(msg='Synchronizing...')
                await sync_commands(yobot)
                log(msg_key='success', success='Synchronization')


        case 'avatar':
            log(msg_key='terminal_callback', command=cmd)
            change_avatar = get_boolean_input('Do you want to change the avatar? (y/n) ')
            if change_avatar:
                await set_avatar(yobot)
                log(msg='Avatar changed!')


        case 'botname':
            log(msg_key='terminal_callback', command=cmd)
            change_botname = get_boolean_input('Do you want to change YoBots name? (y/n) ')
            if change_botname:
                new_name = input('Enter new bot name: ')
                await set_display_name(yobot, display_name=new_name)


        case 'status':
            log(msg_key='terminal_callback', command=cmd)
            change_status = get_boolean_input('Do you want to change the status? (y/n) ')
            if change_status:
                await yobot.bot.change_presence(activity=discord.Game(yobot.bot.now_playing))
                log(msg='Status changed!')


        case _:
            log(msg_key='terminal_callback', command=cmd)
            log(msg_key='error', error=f"Invalid command: {cmd}")