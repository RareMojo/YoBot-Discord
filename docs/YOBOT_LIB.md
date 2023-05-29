# YoBot Management Functions

This script provides functions for managing the `YoBot`, a Discord bot. 

The functionalities covered by these functions include updating the bot's settings, setting a welcome message, and changing the bot's properties from the terminal.

## Function Descriptions

### `update_yobot(yobot)`
- This asynchronous function updates `YoBot`'s name, presence, and avatar to the values defined in its configuration file across all Discord servers. It checks whether an update is needed and applies it if so, updating the configuration file as needed.

### `welcome_to_yobot(yobot)`
- This asynchronous function displays a welcome message in the terminal.
    It includes details of the bot's current state, such as its display name and presence, and the guilds (Discord servers) it is connected to.

### `exit_bot_terminal(yobot)`
- This function stops the bot when called from the terminal.

### `set_bot_name(yobot)`
- This asynchronous function allows the bot's name to be changed from the terminal.
    It updates both the bot's configuration file and its display name on Discord servers.

### `set_bot_avatar(yobot)`
- This asynchronous function changes the bot's avatar from the terminal.
    It updates the bot's configuration file and its avatar on Discord servers.

### `set_bot_presence(yobot)`
- This asynchronous function changes the bot's presence from the terminal.
    It updates both the configuration file and the bot's presence on Discord servers.

### `sync_commands(yobot)`
- This asynchronous function synchronizes the bot's commands from the terminal with the ones on Discord servers.

### `set_owner(yobot)`
- This asynchronous function allows the bot's owner to be changed from the terminal.
    It updates both the bot's configuration file and the bot's owner information.

### `ping(yobot)`
- This function simply returns a "Pong!" message, used to test the bot's responsiveness.

### `show_help(yobot)`
- This function displays a help menu in the terminal, listing all the available commands for managing the bot.

### `get_boolean_input(yobot, prompt)`
- This function gets a boolean input from the user.
    It continues to prompt the user until a valid '`yes`' or '`no`' response is given.

#### Please note, to run these functions, you'll need a running instance of YoBot to pass as the yobot parameter.