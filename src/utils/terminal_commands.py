from typing import TYPE_CHECKING

from utils.yobotlib import (download_cogs, exit_bot_terminal, list_cogs, ping,
                            remove_cogs, set_bot_avatar, set_bot_name,
                            set_bot_presence, set_owner, show_aliases,
                            show_help, sync_commands, wipe_config)

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
            exit_bot_terminal(self.yobot)

        elif user_command in ['help', 'h', '?']:
            show_help(self.yobot)

        elif user_command in ['ping', 'p']:
            ping(self.yobot)

        elif user_command in ['setbotname', 'setbot', 'sbn']:
            await set_bot_name(self.yobot)

        elif user_command in ['setbotpresence', 'setbotpres', 'sbp']:
            await set_bot_presence(self.yobot)

        elif user_command in ['setbotavatar', 'setava', 'sba']:
            await set_bot_avatar(self.yobot)

        elif user_command in ['setowner', 'setown']:
            await set_owner(self.yobot)

        elif user_command in ['reload', 'sync', 'r']:
            await sync_commands(self.yobot)

        elif user_command in ['wipebot', 'wipeconfig', 'wipe', 'wb']:
            wipe_config(self.yobot)

        elif user_command in ['getcog', 'getcogs', 'gc']:
            download_cogs(self.yobot, self.yobot.cogs_dir)
            await self.yobot.load_cogs()
            await sync_commands(self.yobot)

        elif user_command in ['removecog', 'removecogs', 'rc']:
            remove_cogs(self.yobot, self.yobot.cogs_dir)
            
        elif user_command in ['listcogs', 'list', 'lc']:
            list_cogs(self.yobot, self.yobot.cogs_dir)
        
        elif user_command in ['alias', 'aliases', 'a']:
            show_aliases(self.yobot)
            
        else:
            print(f"'{user_command}' is not a recognized command.")
