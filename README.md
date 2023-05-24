# #YoBot
<br>

The YoBot project is a structured and customizable bot framework implemented in Python. 

It comes prepared to with a localized terminal, extension loading, examples, and other essentials.

The structure of the project and functionalities of each module are described below.
<br>
<br>

## #Features
### Accessibility
Yobot is meant to be easy to setup and use without much know how. Today it may be a few foreign commands, tomorrow it will be seamless for anyone.

This can serve as a template to quickly deploy a barebones Discord.py bot without much hassle.

It's also intended to be a great learning tool for anyone that is looking for an easy programming project.

Designing an Extension isn't rocket science. The limit is your creativity!
<br>
<br>

### OS Compatibility
YoBot is designed to function on both Windows and Linux out of the box.

There are no plans to make support for any other platforms.
<br>
<br>

### Languages Support
YoBot has multilingual support, which is achieved by using JSON files for each supported language.

Each JSON file contains system messages translated into the respective language.

The Discord and other API handlers can often do their own localization, but this handles the local terminal system.

<b>Note:</b> *machine translated, may not be accurate*
<br>
<br>

### Logging
YoBot uses Python's built-in logging module that records and saves events that occur while YoBot is running.

It's designed with an optional key system to easily edit system level messages and add localization.

The log messages can be formatted to your desire here.
<br>
<br>

### Terminal Command Handling
YoBot can handle commands entered directly from the terminal.

The included commands include exit, help, language, and ping.

You can easily create new commands for the terminal.

This allows YoBot to still be utilized as a regular Python-bot at its core.

<b>Note:</b> *please follow security guidelines*
<br>
<br>

### Extensions
Extensions are intended for additional modular features to extend the functionality of YoBot.

These can be `Cogs`, `Events`, or `Plugins`.

Each Extension is expected to be a separate Python script implementing a particular feature or set of features.

This can be something as simple as custom Discord commands to tracking every Elon Musk tweet in your private server.
<br>
<br>

## #Installation
### Prerequisites
- Discord, Discord Account, and Discord App
- Python 3.10.9+
- requirements.txt
- IDE of choice if you want to extend the app (VSCode is my goto)

1. ### Clone the repository:
    - `git clone https://github.com/RareMojo/yobot`

2. ### Install the required dependencies:
    - `pip install -r requirements.txt`

3. ### Invite YoBot:
    - Visit here and create an application. https://discord.com/developers/applications
    - Obtain a secret token for the config file.
    - Follow this guide for more info. https://discordjs.guide/preparations/adding-your-bot-to-servers.html#bot-invite-links

4. ### Run YoBot:
    - When launching the first time it will automatically ask you for inputs to configure YoBot.
    - You <b>MUST</b> have your `discord_token` at a minimum for this step.
    - Run `python .\main.py` to launch YoBot.
    - If you encounter any issues, please refer to the logging information outputted to the console or written to the log file.

5. ### Edit and Add
    - Add modules to the `data/Cogs` directory to extend functionality.
    - Add or edit anything you'd like.
<br>

## #Configuration Management
Configuration settings for YoBot are stored in INI files in the configs directory.

The `core_config.ini` file stores settings related to YoBot's core functionalities, while the `bot_config.ini` file stores settings specifically related to the Discord bot functionalities.

### Core Configuration
- `owner_name` Is the name of the person hosting this.
- `debug` Is the developer mode toggle.
- `language` The core language all `msg_key` log messages will follow.

### Bot Configuration
- `discord_token` Is the app secret key.
- `display_name` Sets YoBots name.
- `now_playing` Sets the now playing message.
- `intents` Sets YoBot permission level.
- `data/images/avatar.png` Swap for any 128x128 png/jpg to change avatars.

### Project Structure
- `Root Directory:` Contains the main Python scripts for launching and setting up YoBot, as well as the following subdirectories:
    - `resources:` Contains all bot resources such as images, sounds, and texts. This includes things such as system text, avatars, and etc.
    - `configs:` Contains INI configuration files for YoBot and core functionalities.
    - `data:` Stores general data. Unused currently. Planned for any Cog or Discord data storage.
    - `logs:` The location for storing log files.
    - `src:` Contains the main source code for YoBot's features, divided into separate modules, including Cogs.
        - `bot:` This is where YoBot is stored. Contains anything especially particular for YoBot.
        - `events:` This is where all Discord related events will be stored. Unused currently.
        - `cogs:` This is where all Cogs will be stored.
        - `utils` Contains helper functions for YoBot framework.
<br>

# #The Code
Here is a brief description of what is going on under the hood so that you can get started.

For more information, look into the code. There should be docstrings to help guide you.
<br>
<br>

## yobot.py
This is where the main YoBot class is defined. This class is derived from a superclass `discord.ext.commands.Bot`.

When the class is instantiated, it creates a new instance of the YoBot class.

The project refers to the instantiated YoBot as `self`, `yobot`, or `self.yobot`.

These variables will represent the running instance of YoBot with all of its settings.

<br>

## main.py
This script is where YoBot is launched from. It imports the YoBot class from `yobot.py` and the `setup_bot()` function from `setup.py`, and uses them to launch YoBot.

It only serves as a seperate entry point for YoBot to begin.

<br>

## setup.py
This is responsible for setting up the file structure, terminal, logging, configuration files, and returning a ready-to-start bot instance. 

All functions in here have the goal of making a ready bot only.

#### Key Functions:
- `setup_bot()`: Sets up YoBot and returns a ready-to-start bot instance.
- `setup_logging()`: Sets up the logging module and returns a logger instance.
- `setup_cogs()`: Loads all available Cogs and Events into the loaded bot instance.

<br>

## yobotlib.py
This script includes helper functions for the entire YoBot project. It is imported by all other scripts.

#### Key Functions:

- `log():` Logs a formatted message based on a message key or string argument.
- `update_config():` Updates a config file without overwriting other keys.
- `sync_commands():` Syncs the Discord commands with the Cogs modules.

<br>

## terminal_commands.py
This is where all of the terminal commands are setup. Quickly change or add commands for the terminal.

These commands are not part of the YoBot framework. They are only for the terminal.

It is not advised to allow the YoBot or any Cog/Extension to use these commands.

#### Key functions:
- `handle_terminal_command():` The terminal listens to anything in this list and will execute the block the case matches. Has built-in command callback response.
- `set_language():` Sets the language of the terminal messages. (Not Discord)

<br>

# #Extensions
Extensions are Events, Cogs, and Plugins. These are drop in and out modules for YoBot to process.

With these, YoBot can be very customizable and solve multiple problems.

Below is a brief description of some of the ones that come included.

<br>

## discordcommandscog.py

This is where all of the Discord commands are setup.
Quickly change or add commands for the Discord bot.

<br>

## discordevents.py

Events are listeners. Quickly change or add events for the Discord bot.
You can tap into a listening event and add functionality to it.

#### Key functions:
- `on_connect():` This fires when YoBot is connected to Discord.
- `on_ready():` This fires when YoBot is ready to be used.
- `on_message():` This fires anything in this block when a message is received.

<br>
    
## #Thank You
Thank you for your interest in the YoBot project. This endeavor is a product of commitment to providing a customizable, user-friendly bot.

I hope this detailed overview provided useful insights into the inner workings of YoBot. 

If you have any questions, suggestions, or require further information, don't hesitate to reach out. Your involvement makes YoBot better.

Once again, thank you for your time. 

Happy Coding!
<br>
<br>

## License
MIT License

Copyright (c) 2023 Nick Rejcek

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
