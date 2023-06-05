from typing import TYPE_CHECKING

from utils.yobotlib import (add_blacklist, download_cogs, exit_bot_terminal,
                            list_cogs, ping, remove_blacklist, remove_cogs,
                            set_bot_avatar, set_bot_name, set_bot_presence,
                            set_owner, show_aliases, show_help, sync_commands,
                            toggle_debug_mode, verify_all_cogs, wipe_config, toggle_dev_mode)

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

        elif user_command in ['setbotpresence', 'setbotpres', 'sbp']:
            self.yobot.log.debug('Setting bot presence...')
            await set_bot_presence(self.yobot)

        elif user_command in ['setbotavatar', 'setava', 'sba']:
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
            download_cogs(self.yobot, self.yobot.cogs_dir,
                          self.yobot.cogs_sigs_dir, self.yobot.config['repo_info'])
            await self.yobot.load_cogs()
            await sync_commands(self.yobot)

        elif user_command in ['removecog', 'removecogs', 'rc']:
            self.yobot.log.debug('Removing cogs...')
            remove_cogs(self.yobot, self.yobot.cogs_dir)

        elif user_command in ['listcogs', 'list', 'lc']:
            self.yobot.log.debug('Listing cogs...')
            list_cogs(self.yobot, self.yobot.cogs_dir)

        elif user_command in ['verifycogs', 'verify', 'vc']:
            self.yobot.log.debug('Verifying cogs...')
            verify_all_cogs(self.yobot, self.yobot.cogs_dir,
                            self.yobot.cogs_keys_dir, self.yobot.cogs_verify_blacklist)

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
            remove_blacklist(self.yobot)

        else:
            self.yobot.log.info(
                f"'{user_command}' is not a recognized command.")
