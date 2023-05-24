import asyncio

from discord.ext import commands

from utils.setup import setup_cogs
from utils.terminal_commands import terminal_command_loop
from utils.yobotlib import log


class YoBot(commands.Bot):
    """Initializes a new instance of the YoBot class with the given parameters."""
    def __init__(self, intents, display_name, now_playing, discord_token, avatar):
        super().__init__(command_prefix='/', intents=intents)

        # YoBot parameters
        self.running = True

        # Discord parameters
        self.display_name = display_name
        self.now_playing = now_playing
        self.discord_token = discord_token
        self.avatar = avatar


    # YoBot core - unrelated to Discord
    async def start_bot(self):
        """Starts YoBot asynchronously by starting it with the specified Discord token and handling terminal commands."""
        await setup_cogs(self)
        yobot_task = asyncio.create_task(self.start(self.discord_token))
        command_task = asyncio.create_task(terminal_command_loop(self))
        log(msg_key='start')
        
        try:
            while self.running:
                await asyncio.sleep(0)
        except Exception as e:
            log(msg=f"Bot encountered an error: {e}")
        finally:
            yobot_task.cancel()
            command_task.cancel()


    def stop_bot(self):
        """Stops YoBot and sets the running flag to False."""
        log(msg_key='shutdown')
        self.running = False