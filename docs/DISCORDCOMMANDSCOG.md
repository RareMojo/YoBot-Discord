# DiscordCommandsCog Class

The `DiscordCommandsCog` class is a collection of commands that `YoBot` can execute. 

This class inherits from the `commands.Cog` class from `discord.py` library.

## Class Attributes

- `yobot`: This represents an instance of the `YoBot` bot class.

## Class Methods

- `__init__(self, yobot)`

This is the constructor for the `DiscordCommandsCog` class. 

It initializes an instance of the class with a reference to the bot instance (`YoBot`).

## Commands

Commands are methods that can be called directly by users. 

The `@commands.command(name="")` decorator indicates that these methods are commands.

- `ping_command`: This command responds with "Pong!" when a user types "/ping". It's an example of a simple command.
- `admin_command`: This command can only be used by users with an Admin or Moderator role. It's an example of a command that checks the user's role before proceeding.
- `restart`: This command restarts the bot. It first sends a message "Restarting...", then stops and restarts the bot.
- `parent_command`: This is a parent command. It's part of a command group and other commands can be attached to it as "subcommands".
- `sub_command`: This command is a subcommand of the parent_command. It's an example of a command that takes an argument from the user.

## Function

- `async def setup(yobot: commands.Bot) -> None`

This is a standalone asynchronous function which loads the `DiscordCommandsCog` into the bot instance. 

It's typically called during the bot setup process.