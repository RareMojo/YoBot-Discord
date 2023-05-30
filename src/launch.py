import asyncio
import os

from utils.builder import YoBotBuilder


def launch_bot():
    """Launches YoBot."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # The root directory of the project.
    builder = YoBotBuilder(f'{root_dir}/logs/latest.log', # Setup the file paths based on the root directory.
                        f'{root_dir}/configs/config.json',
                        f'{root_dir}/resources/images/avatar.png',
                        f'{root_dir}/src/cogs')
    
    bot = builder.yobot_build() # Build the bot.
    asyncio.run(bot.start_bot())


if __name__ == "__main__":
    launch_bot()