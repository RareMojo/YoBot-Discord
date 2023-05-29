# YoBot Launch Script

This script is responsible for launching the `YoBot` instance.

It sets up the necessary paths for logs, configuration, avatar images and `cog` source files, and then starts the bot.

## Function Descriptions

### `launch_bot()`
- This function launches `YoBot` by first establishing the root directory of the project.
    It then sets up the appropriate file paths for the log file, configuration file, avatar image and `cog` source files based on the root directory.

A `YoBotBuilder` object is created with the aforementioned paths, which is then used to build the `YoBot` instance. This `YoBot` instance is then started using an asyncio event loop.

## Main Execution
The script only executes `launch_bot`() if the script is being run directly (i.e., it's not being imported as a module in another script). This prevents `YoBot` from being unintentionally launched when the module is imported.

To execute this script and launch `YoBot`, navigate to the directory containing this script in a terminal or command prompt and run the command python `script_name.py` (replace `script_name.py` with the actual script's filename).

#### Please note, you'll need an existing YoBot instance and its related files in the specified paths for this script to work correctly.