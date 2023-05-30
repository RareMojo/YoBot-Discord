from typing import TYPE_CHECKING

from utils.yobotlib import (exit_bot_terminal, ping, set_bot_avatar,
                            set_bot_name, set_bot_presence, set_owner,
                            show_help, sync_commands, wipe_config, download_cogs)

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
        
        match user_command:
            case 'exit':
                exit_bot_terminal(self.yobot)
                
            case 'help':
                show_help(self.yobot)
                
            case 'ping':
                ping(self.yobot)
                
            case 'setbotname':
                await set_bot_name(self.yobot)

            case 'setbotpresence':
                await set_bot_presence(self.yobot)
                
            case 'setbotavatar':
                await set_bot_avatar(self.yobot)
            
            case 'setowner':
                await set_owner(self.yobot)

            case 'reload':
                await sync_commands(self.yobot)
                
            case 'wipebot':
                wipe_config(self.yobot)
            
            case 'getcogs':
                download_cogs(self.yobot, self.yobot.cogs_dir)
                await self.yobot.load_cogs()
                await sync_commands(self.yobot)
            
            case _:
                self.yobot.log.warning('Invalid command: {}'.format(user_command))