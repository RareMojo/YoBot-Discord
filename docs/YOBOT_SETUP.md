# YoBotBuilder Class

`YoBotBuilder` is a class used to build an instance of the `YoBot` class. 

It sets up the necessary files and configurations required for the operation of the bot.

Once the files and configurations are set, it builds a new instance of the `YoBot` class to be launched.

## Installation

Like the `YoBotLogger`, `YoBotBuilder` is a custom Python module. 

It's built in with the `YoBotBuilder` class, which is used to build an instance of the `YoBot` class.

## Usage
### YoBotBuilder

You can create a new `YoBotBuilder` instance by providing the following arguments:

```python
yobot_builder = YoBotBuilder(
    yobot,
    'path/to/log/file.log',
    'path/to/config/file.json',
    'path/to/avatar/file.png',
    'path/to/cogs/directory'
)
```

- `yobot`: The `YoBot` class to build.
- `log_file`: The path to the log file.
- `config_file`: The path to the configuration file.
- `avatar_file`: The path to the avatar file.
- `cogs_dir`: The path to the cogs directory.

## Setup Files and Configurations

Before building a `YoBot` instance, ensure to set up the required files and configurations using the following methods:

```python
yobot_builder.setup_files()
yobot_builder.setup_config()
```

- `setup_files`: Sets up the necessary files for `YoBot` to run.
- `setup_config`: Sets up the configuration file for `YoBot`. If the configuration file is not found, it will prompt you to enter the necessary information to create a new configuration file.

## Building YoBot

Once the files and configurations are set, build a new instance of the `YoBot` class using the build method:

```python
yobot = yobot_builder.build()
```