import asyncio
import os

from utils.builder import YoBotBuilder
from utils.yobotlib import update_config

import yaml



def launch_bot():
    """Ensures that the bot's files are set up, then builds and starts the bot."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # The root directory of the project.
    config_dir = f'{root_dir}/configs'
    config_file = f'{root_dir}/configs/config.yaml'
    log_dir = f'{root_dir}/logs'
    log_file = f'{root_dir}/logs/yobot.log'
    avatar_file = f'{root_dir}/resources/images/avatar.png'
    cogs_dir = f'{root_dir}/src/cogs'
    cogs_sigs_dir = f'{root_dir}/src/cogs/sigs'
    cogs_key_file = f'{root_dir}/src/cogs/sigs/cogs_key_public.pem'
    resources_dir = f'{root_dir}/resources'
    images_dir = f'{root_dir}/resources/images'
    sounds_dir = f'{root_dir}/resources/sounds'
    texts_dir = f'{root_dir}/resources/texts'
    
    try:
        try:
            print('Checking for directories...')
            if not os.path.isdir(config_dir):
                os.mkdir(config_dir)
                print('Config directory not found. Creating config directory...')
                
            if not os.path.isdir(log_dir):
                os.mkdir(log_dir)
                print('Log directory not found. Creating log directory...')
                with open(log_file, 'w') as f:
                    f.write('')
                print('Log file not found. Creating log file...')
                
            if not os.path.isdir(cogs_dir):
                os.mkdir(cogs_dir)
                print('Cogs directory not found. Creating cogs directory...')

            if not os.path.isdir(cogs_sigs_dir):
                os.mkdir(cogs_sigs_dir)
                print('Cogs signatures directory not found. Creating cogs signatures directory...')
        except Exception as e:
            print(f'Error creating directories: {e}')
            
        if not os.path.isfile(config_file):
            print('Config file not found. Setting up config...')
            print('Please enter the following information to set up the config file.')
            
            file_paths = {
                "root_dir": root_dir,
                "config_dir": config_dir,
                "config_file": config_file,
                "log_dir": log_dir,
                "log_file": log_file,
                "avatar_file": avatar_file,
                "cogs_dir": cogs_dir,
                "cogs_sigs_dir": cogs_sigs_dir,
                "cogs_key_file": cogs_key_file,
                "resources_dir": resources_dir,
                "images_dir": images_dir,
                "sounds_dir": sounds_dir,
                "texts_dir": texts_dir  
            }
            
            config = {
                "owner_name": input('Owner Name: '),
                "owner_id": input('Owner ID: '),
                "prefix": input('Command Prefix: '),
                "discord_token": input('Discord Token: '),
                "bot_name": input('Bot Name: '),
                "presence": input('Presence: '),
                "log_level": 'INFO',
                "dev_mode": False,
                "update_bot": True,
                "file_paths": file_paths,
                "blacklist": {
                    "cog_removal": ["yobotcorecog.py", "yobotcommandcog.py"],
                    "cog_verify": ["yobotcorecog.py", "yobotcommandcog.py"]
                }
            }


            with open(config_file, 'w') as f:
                yaml.dump(config, f)
            print('Config file created.')
        else:
            print('Config file found.')          
    except Exception as e:
        print(f'Error setting up YoBot files: {e}')

    # load the config file
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    builder = YoBotBuilder(config_file=config_file)
    
    yobot = builder.yobot_build() # Build the bot.
    if yobot:
        asyncio.run(yobot.start_bot())
    else:
        print('YoBot failed to build or start.')
        input('Press ENTER to EXIT.')
        

if __name__ == "__main__":
    launch_bot()