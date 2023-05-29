# YoBot
<br>

The `YoBot` project is a basic, structured, and customizable bot framework implemented in [Discord.py](https://discordpy.readthedocs.io/en/stable/api.html) 2.0+. 

It comes prepared with a localized terminal, extension loading, examples, and other essentials.

The structure of the project and functionalities of each module are described below.
<br>
<br>

## Features
### Accessibility
`YoBot` is meant to be easy to setup and use without much know how. Today it may be a few foreign commands, tomorrow it will be seamless for anyone.

This can serve as a template to quickly deploy a barebones [Discord.py](https://discordpy.readthedocs.io/en/stable/api.html) 2.0+ bot without much hassle.

It's also intended to be a great learning tool for anyone that is looking for an easy programming project.

Designing a [Cog](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html) isn't rocket science. The limit is your creativity!
<br>
<br>

### OS Compatibility
`YoBot` is designed to function on both Windows and Linux out of the box.

There are no plans to make support for any other platforms.
<br>
<br>

### Logging
`YoBot` uses a custom logging module to handle all logging.

This allows for changing the way logs are saved, formatted, and handled easily.
<br>
<br>

### Terminal Command Handling
`YoBot` can handle commands entered directly from the terminal.

Some included commands are `exit`, `help`, `setbotname`, and more.

You can easily create new commands for the terminal.

Start creating them in `yobot_logger.py` within class `YobotTerminalCommands()` by calling functions from `yobot_lib.py`.

This allows `YoBot` to still be utilized as a regular Python-bot at its core.

<b>Note:</b> *please follow security guidelines*
<br>
<br>

### Extensions
Extensions are intended for additional modular features to extend the functionality of `YoBot`.

These are called [Cogs](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html) and can be a number of things.

Each [Cog](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html) is expected to be a separate Python script implementing a particular feature or set of features.

This can be something as simple as custom Discord commands to tracking every Elon Musk tweet in your private server.
<br>
<br>

## Installation
### Prerequisites
- Discord Account, and [Discord App](https://discord.com/)
- [Python 3.10.9+](https://www.python.org/downloads/)
- requirements.txt
- IDE of choice if you want to extend the app ([VSCode](https://code.visualstudio.com/) is my goto)

1. ### Clone the repository:
    - `git clone https://github.com/RareMojo/YoBot-Discord`

2. ### Install the required dependencies:
    - `pip install -r requirements.txt`

3. ### Invite `YoBot`:
    - Visit [Discord Developer Portal](https://discord.com/developers/applications) and create an application.
    - Obtain a secret token for the config file.
    - Follow [this guide](https://discordjs.guide/preparations/adding-your-bot-to-servers.html#bot-invite-links) for more info.

4. ### Run `YoBot`:
    - When launching the first time it will automatically ask you for inputs to configure `YoBot`.
    - You <b>MUST</b> have your `discord_token` at a minimum for this step. *NEVER SHARE THIS TOKEN*
    - Run `python .\main.py` to launch `YoBot`.
    - If you encounter any issues, please refer to the logging information outputted to the console or written to the log file.

5. ### Edit and Add
    - Add modules to the `src/cogs` directory to extend functionality.
    - Add or edit anything you'd like.
<br>

## Configuration Management
Configuration settings for `YoBot` are stored in the `/configs` directory as JSON files.

The `config.json` file contains the main configuration settings for `YoBot`.

Change your avatar in `resources/images/avatar.png`. Swap for any 128x128 png/jpg.

*Never share your configs, tokens, ids, or other sensitive information online*

### Configuration file
- `discord_token` Is the app secret key.
- `owner_name` Sets `YoBot` owner name.
- `owner_id` Sets `YoBot` owner ID.
- `prefix` Sets `YoBot` command prefix.
- `bot_name` Sets `YoBot` name.
- `presence` Sets the now playing message.
- `debug` Sets the debug mode for `YoBot`.
- `update_bot` Flag used for first time setup or updating `YoBot` with new settings.

### Project Structure
- `YoBot-Discord:` Root directory, contains the main Python scripts for launching and setting up `YoBot`, as well as the following subdirectories:
    - `resources:` Contains all `YoBot` resources such as images, sounds, and texts.
    - `configs:` Contains JSON configuration files for `YoBot`. *DO NOT SHARE THIS FILE*
    - `logs:` The location for storing log files.
    - `src:` Contains the main source code for `YoBot`'s features, divided into separate modules, including `Cogs`.
        - `bot:` This is where `YoBot` is stored. Contains anything especially particular for `YoBot`.
        - `cogs:` This is where all `Cogs` will be stored.
        - `utils` Contains utility functions for `YoBot`.
<br>

## Further Documentation
- [All Docs](https://github.com/RareMojo/YoBot-Discord/wiki)

<br>
    
## Thank You
Thank you for your interest in the `YoBot` project. This endeavor is a product of commitment to providing a customizable, user-friendly bot.

I hope this detailed overview provided useful insights into the inner workings of `YoBot`. 

If you have any questions, suggestions, or require further information, don't hesitate to reach out. Your involvement makes `YoBot` better.

Once again, thank you for your time. 

Happy Coding!
<br>
<br>

## License
`YoBot` is licensed under the MIT License.
You are free to use, modify, and distribute `YoBot` as you see fit.
However, there are certain restrictions on the use of the `YoBot` name, logo, and code.
See `LICENSE.md` for details.
