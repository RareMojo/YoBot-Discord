# YoBot
<br>

The YoBot project is a basic, structured, and customizable bot framework implemented in [Discord.py](https://discordpy.readthedocs.io/en/stable/api.html) 2.0+. 

It comes prepared with a localized terminal, extension loading, examples, and other essentials.

The structure of the project and functionalities of each module are described below.
<br>
<br>

## Features
### Accessibility
YoBot is meant to be deployed by anyone without any knowledge of Python or Discord.py, or programming.

The base bot has some basic functionality and can be used as is.

You can download pre-made extensions to add more features to your bot without any programming knowledge.

You can even try to create your own extensions without touching <i>ANY</i> of the source code.

Creating a Cog extension is a great way to learn Python and Discord.py without having to worry about the rest of the bot.
<br>
<br>

### Extensions
Extensions are intended for additional modular features to extend the functionality of YoBot.

These are called [Cogs](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html) and can be a number of things.

Each [Cog](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html) is expected to be a separate Python script implementing a particular feature or set of features.

This can be something as simple as custom Discord commands to tracking every Elon Musk tweet in your private server.
<br>
<br>
    
### OS Compatibility
YoBot is designed to function on both Windows and Linux out of the box.

There are no plans to make support for any other platforms at this time.
<br>
<br>

### Logging
YoBot uses a custom logging module to handle the terminal log and log files.

This should allow some flexibility for these built in features for other developers.
<br>
<br>

### Terminal Command Handling
YoBot can handle commands entered directly from the terminal for more control.

This means YoBot can be used as a standalone application without Discord as well.

These commands allow for great customizability and control without digging through config files at all.

You can easily create new commands for the terminal and it is another great way to learn Python without having to worry about the rest of the bot.

Start creating them in `terminalcommands.py` within class `YobotTerminalCommands()` by calling/creating functions in `yobotlib.py`.

<b>Note:</b> *please follow security guidelines*
<br>
<br>

## Usage

For complete usage please see the [YobotWiki](https://github.com/RareMojo/YoBot-Discord/wiki).

<br>

### Quick Start

### Installation

Installation is simple and only requires a few steps.

We have a few options depending on your ambitions.

- See the install guide [here](https://github.com/RareMojo/YoBot-Discord/wiki/Installation)

<br>

### Configuration

Configuration is simple and only requires a few steps.

It is done automatically at launch and requires user input for a few required fields.

You can also edit the config file directly or using various terminal commands.

See more information [here](

<br>
<br>

## Thank You
Thank you for being interested in the YoBot-Discord project! 

We're dedicated to creating a bot that's easy to customize and use, both for programmers and regular users.

I hope the information I shared about YoBot gave you a good understanding of how it works.

If you have any questions, suggestions, or need more information, feel free to get in touch. 

Your input is valuable and helps us improve YoBot.

Thanks again for your time and happy coding!
<br>
<br>

## License
YoBot is completely open source, licensed under the [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html) license.
See LICENSE.md for more information.