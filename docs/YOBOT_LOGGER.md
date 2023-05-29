# YoBotLogger Class

The `YoBotLogger` package provides a custom logging functionality for applications, specifically for a bot called "`YoBot`".

The package inherits from Python's built-in logging module and offers features such as:

- Custom log formatting
- File rotation (`RotatingFileHandler`)
- Terminal command handling

## Installation

As `YoBotLogger` is a custom Python module.

It's built in with the `YoBotBuilder` class, which is used to build an instance of the `YoBot` class.

## Usage
### YoBotLogger

`YoBotLogger` is the main class which sets up the logger.

```python
logger = YoBotLogger(
    name='your_logger_name',
    log_file='path/to/log/file.log',
    level=logging.INFO, 
    maxBytes=1000000, 
    backupCount=1
)
```

- `name`: The name of the logger.
- `log_file`: The path to the log file.
- `level`: The logging level (default: `logging.INFO`).
- `maxBytes`: The maximum size of a log file. After reaching this limit, the log file will be rotated (default: `1000000`).
- `backupCount`: The number of backup log files to keep (default: `1`).

## Terminal Command Loop

You can initiate the main `YoBotLogger` terminal command loop by calling the `terminal_command_loop` function.

```python
async def main():
    await terminal_command_loop(yobot)

asyncio.run(main())
```

## Terminal Commands

`YoBotLogger` terminal commands are handled by the `YobotTerminalCommands` class. 

These commands are meant to be <b>uni-directional</b>.

```python
command_handler = YobotTerminalCommands(yobot, 'your_command')
await command_handler.handle_terminal_command()
```

The terminal commands supported are:

- `exit`: Exits the bot terminal.
- `help`: Shows help.
- `ping`: Pings the bot.
- `setbotname`: Sets the bot name.
- `setbotpresence`: Sets the bot presence.
- `setbotavatar`: Sets the bot avatar.
- `setowner`: Sets the owner.
- `reload`: Syncs commands.