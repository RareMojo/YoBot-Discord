# YoBot Class

This class represents the main `YoBot` bot class that handles initialization and startup.

It inherits from the `commands.Bot` class of the `discord.ext` module, and contains multiple methods and attributes to manage the bot's operation.

<br>

## Class Attributes
- `config` (dict): Stores the bot's configuration file.
- `config_file` (str): Holds the path to the bot's configuration file.
- `avatar` (str): Holds the path to the bot's avatar file.
- `cogs_dir` (str): Holds the path to the bot's `cogs` directory.
- `bot_name` (str): Contains the bot's name.
- `presence` (str): Contains the bot's presence.
- `owner_name` (str): Contains the bot owner's name.
- `owner_id` (str): Contains the bot owner id.
- `log` (`YoBotLogger`): The bot's logger instance.
- `running` (bool): A flag to indicate whether the bot is currently running.

<br>

## Class Methods

#### `__init__(self, intents, logger, config_file, avatar, cogs_dir)`
- The constructor for the `YoBot` class. 
    It initializes an instance of the class with the given parameters.
    The configuration file is loaded during this initialization process.

#### `start_bot(self)`
- This method starts the bot.
    It first loads all `cogs`, and then initiates two asynchronous tasks - starting the bot and starting the terminal command loop.

#### `stop_bot(self)`
- This method stops the bot.
    It sets the running flag to False.

#### `load_cogs(self)`
- This method loads all the `cogs` in the cogs directory.
    Each cog is an extension that adds functionality to the bot.
    This function goes through each file in the specified cogs directory, and loads any files that end with '`cog.py`' as a bot extension.

<br>

## Execution

- The `YoBot` class doesn't include any script execution itself - it's designed to be imported and utilized in other Python scripts. To make use of this class, create an instance of `YoBot` in your script, and call the `start_bot()` method to start the bot.
