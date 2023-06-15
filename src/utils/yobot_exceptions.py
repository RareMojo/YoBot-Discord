class YoBotException(Exception):
    """Base class for exceptions in YoBot."""
    pass

class ConfigException(YoBotException):
    """Exception raised for errors in the configuration file."""
    def __init__(self, config_file, message):
        self.config_file = config_file
        super().__init__(f"Error in config file {config_file}: {message}")

class CogException(YoBotException):
    """Exception raised for errors related to cogs."""
    def __init__(self, cog_name, message):
        self.cog_name = cog_name
        super().__init__(f"Error with cog {cog_name}: {message}")

class CommandException(YoBotException):
    """Exception raised for errors in commands."""
    def __init__(self, command_name, message):
        self.command_name = command_name
        super().__init__(f"Error with command {command_name}: {message}")

class BotBuildException(YoBotException):
    """Exception raised for errors in building the bot."""
    def __init__(self, component, message):
        self.component = component
        super().__init__(f"Error building bot component {component}: {message}")

class LoggerException(YoBotException):
    """Exception raised for errors in the logging system."""
    def __init__(self, log_file, message):
        self.log_file = log_file
        super().__init__(f"Error with log file {log_file}: {message}")

class FileException(YoBotException):
    """Exception raised for errors related to files."""
    def __init__(self, file_name, message):
        self.file_name = file_name
        super().__init__(f"Error with file {file_name}: {message}")