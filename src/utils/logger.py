import asyncio
import logging
import os
import re
from logging.handlers import RotatingFileHandler

from utils.yobotlib import exit_bot_terminal, set_bot_name, set_bot_avatar, set_bot_presence, set_owner, sync_commands, ping, show_help 


class YoBotLogger(logging.Logger):
    """
    Sets up the YoBotLogger class.
    
    This class inherits from the logging.Logger class.
    It provides a custom logging format, file rotation, and terminal input/output.

    Args:
        name (str): The name of the logger.
        log_file (str): The path to the log file.
        level (int): The logging level.
        maxBytes (int): The maximum number of bytes before the log file is rotated.
        backupCount (int): The number of log files to keep.
    """
    def __init__(self, name: str, log_file: str, level: int = logging.INFO, maxBytes: int = 1000000, backupCount: int = 1):
        super().__init__(name, level)
        self.log_file = log_file
        self.name = name
        self.level = level
        self.maxBytes = maxBytes
        self.backupCount = backupCount
        self.setup_logger()
    
    def setup_logger(self):
        """Sets up the logger."""
        file_handler = YoLoggerRotater(log_file=self.log_file, maxBytes=self.maxBytes, backupCount=self.backupCount) # Setup the file rotater.
        file_handler.setFormatter(YoLoggerFormat()) # Setup the file formatter.
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(YoLoggerFormat())
        
        self.setLevel(self.level) # Set the logging level.
        file_handler.setLevel(self.level)
        console_handler.setLevel(self.level)

        self.addHandler(file_handler) # Add the handlers.
        self.addHandler(console_handler)
        

class YoLoggerFormat(logging.Formatter):
    """Provides a custom logging format."""
    black = "\x1b[30m"
    red = "\x1b[31m"
    purple = "\x1b[35m"
    cyan = "\x1b[36m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    gray = "\x1b[38m"
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: cyan + bold,
        logging.INFO: green + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red + bold,
        logging.CRITICAL: red + bold,
    }

    def format(self, record: logging.LogRecord):
        """Formats the log message."""
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname: <8}(black)[(reset)(purple)YoBot(black)] >(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(gray)", self.gray + self.bold)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(purple)", self.purple + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


class YoLoggerRotater(RotatingFileHandler):
    """
    Provides a custom log file handler. 
    
    This class is used to swap the log file with a new one when YoBot is launched.
    
    Args:
        log_file (str): The path to the log file.
        mode (str): The file mode.
        maxBytes (int): The maximum number of bytes before the log file is rotated.
        backupCount (int): The number of log files to keep.
        encoding (str): The encoding to use.
    """
    def __init__(self, log_file: str, mode='a', maxBytes=0, backupCount=0, encoding=None):
        """Handles file swap before beginning to write to the log file."""
        self.log_file = log_file
        if os.path.isfile(self.log_file):
            if os.path.isfile(os.path.join(os.path.dirname(self.log_file), 'old.log')):
                os.remove(os.path.join(os.path.dirname(self.log_file), 'old.log'))
            os.rename(self.log_file, os.path.join(os.path.dirname(self.log_file), 'old.log'))
            
        super().__init__(log_file, mode, maxBytes, backupCount, encoding)
        self.mode = mode
        self.backupCount = backupCount
        self.encoding = encoding

    def emit(self, record: logging.LogRecord):
        """Writes the log record to the latest log, stripping ANSI escape sequences."""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        try:
            msg = self.format(record)
            msg = ansi_escape.sub('', msg)
            with open(self.baseFilename, 'a', encoding='utf-8') as f:
                f.write(msg + self.terminator)
        except Exception:
            self.handleError(record)


async def terminal_command_loop(yobot):
    """The main YoBotLogger terminal command loop."""
    loop = asyncio.get_event_loop()
    delay = 0.25 # The amount of time to wait between each loop.
    launch_delay = 3 # The amount of time to wait for YoBot to finish launching.
    black = YoLoggerFormat.black
    purple = YoLoggerFormat.purple
    bold = YoLoggerFormat.bold
    reset = YoLoggerFormat.reset
    
    if yobot.running:
        await asyncio.sleep(launch_delay) # Wait for YoBot to finish launching.
        
    while yobot.running:
        await asyncio.sleep(delay) # Prevents the terminal from using too much CPU.
        terminal_format = f'{black}{bold}[{purple}YoBot{reset}{black}{bold}]{reset} {yobot.owner_name}{bold}{black}@{reset}{yobot.bot_name}{reset}'
        terminal_prompt = f'{terminal_format}{black}{bold}: > {reset}'
        terminal_command = loop.run_in_executor(None, input, terminal_prompt) # Get the terminal command.
        command_handler = YobotTerminalCommands(yobot, await terminal_command) # Handle the terminal command.
        await command_handler.handle_terminal_command()


class YobotTerminalCommands():
    """
    This class handles YoBotLogger terminal commands.
    These commands are meant to be uni-directional. 

    Args:
        yobot (Yobot): The Yobot instance.
        terminal_command (str): The terminal command.
    """
    def __init__(self, yobot, terminal_command: str):
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
            
            case _:
                self.yobot.log.warning('Invalid command: {}'.format(user_command))