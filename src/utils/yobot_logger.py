import asyncio
import logging
import os
import re
from logging.handlers import RotatingFileHandler
from typing import TYPE_CHECKING

from utils.yobot_terminal import YoBotTerminalCommands

if TYPE_CHECKING:
    from bot.yobot import YoBot


class YoBotLogger(logging.Logger):
    """
    Sets up the YoBotLogger class.

    This class inherits from the logging.Logger class.
    It provides a custom logging format, file rotation, and terminal input/output.

    Args:
        name (str): The name of the logger.
        log_file (str): The path to the log file.
        level (str): The logging level.
        maxBytes (int): The maximum number of bytes before the log file is rotated.
        backupCount (int): The number of log files to keep.
    """

    def __init__(self, name: str, log_file: str, level: str = 'INFO', maxBytes: int = 1000000, backupCount: int = 1):
        super().__init__(name, level.upper())  # Convert level to uppercase string
        """Sets up the YoBotLogger class."""
        self.log_file = log_file
        self.name = name
        self.level = level  # type: ignore # Set the logging level.
        self.maxBytes = maxBytes
        self.backupCount = backupCount
        self.setup_logger()

    def setup_logger(self):
        """Sets up the logger."""
        file_handler = YoBotLoggerRotator(
            log_file=self.log_file, maxBytes=self.maxBytes, backupCount=self.backupCount)  # Setup the file rotater.
        # Setup the file formatter.
        file_handler.setFormatter(YoBotLoggerFormat())
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(YoBotLoggerFormat())

        self.setLevel(self.level)  # Set the logging level.
        file_handler.setLevel(self.level)
        console_handler.setLevel(self.level)

        self.addHandler(file_handler)  # Add the handlers.
        self.addHandler(console_handler)


class YoBotLoggerFormat(logging.Formatter):
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

    def format(self: 'YoBotLoggerFormat', record: logging.LogRecord):
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


class YoBotLoggerRotator(RotatingFileHandler):
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
                os.remove(os.path.join(
                    os.path.dirname(self.log_file), 'old.log'))
            os.rename(self.log_file, os.path.join(
                os.path.dirname(self.log_file), 'old.log'))

        super().__init__(log_file, mode, maxBytes, backupCount, encoding)
        """Sets up the YoBotLoggerRotator class."""
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

async def terminal_command_loop(yobot: 'YoBot'):
    """The main YoBotLogger terminal command loop."""
    loop = asyncio.get_event_loop()
    delay = 0.25  # The amount of time to wait between each loop.
    # The amount of time to wait for YoBot to finish launching.
    launch_delay = 3.5
    black = YoBotLoggerFormat.black
    purple = YoBotLoggerFormat.purple
    bold = YoBotLoggerFormat.bold
    reset = YoBotLoggerFormat.reset

    if yobot.running:
        # Wait for YoBot to finish launching.
        await asyncio.sleep(launch_delay)

    while yobot.running:
        # Prevents the terminal from using too much CPU.
        await asyncio.sleep(delay)
        terminal_format = f'{black}{bold}[{purple}YoBot{reset}{black}{bold}]{reset} {yobot.owner_name}{bold}{black}@{reset}{yobot.config_file.get("bot_name")}{reset}'
        terminal_prompt = f'{terminal_format}{black}{bold}: > {reset}'
        # Get the terminal command.
        terminal_command = loop.run_in_executor(None, input, terminal_prompt)
        # Handle the terminal command.
        command_handler = YoBotTerminalCommands(yobot, await terminal_command)
        await command_handler.handle_terminal_command()
