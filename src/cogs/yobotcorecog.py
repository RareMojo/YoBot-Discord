from typing import TYPE_CHECKING

import discord.ext.commands as commands

from utils.yobotlib import update_yobot, welcome_to_yobot

if TYPE_CHECKING:
    from bot.yobot import YoBot


class YoBotCoreCog(commands.Cog, name='YoBot Core', description='Core Discord event functionality for YoBot.'):
    """Discord events for YoBot to listen to.
    
    Attributes:
        yobot (YoBot): The YoBot instance.
    """
    def __init__(self: 'YoBotCoreCog', yobot: 'YoBot'):
        self.yobot = yobot


    @commands.Cog.listener()
    async def on_connect(self):
        """Called when YoBot connects to Discord."""
        try:
            await update_yobot(self.yobot) # Update YoBot's status and activity, if applicable.
            self.yobot.log.debug('YoBot connected to Discord.')
        except Exception as e:
            self.yobot.log.error(f'Error updating YoBot: {e}')


    @commands.Cog.listener()
    async def on_ready(self):
        """Called when YoBot is ready and connected to Discord."""
        try:
            await welcome_to_yobot(self.yobot) # Send a welcome message to the console.
            self.yobot.log.debug('YoBot is ready and connected to Discord.')
        except Exception as e:
            self.yobot.log.error(f'Error welcoming YoBot: {e}')


    @commands.Cog.listener()
    async def on_message(self, message):
        """Called when a message is received."""
        try:
            if message.author == self.yobot.user: # Ignore messages from the bot itself
                return
            
            #log(f'Message by {message.author} in {message.channel}: {message.content}') ## This is very spammy, so it's commented out by default.

            # Example of a message handler
            if message.content.startswith('hello'):
                await message.channel.send('Hello!')
        except Exception as e:
            self.yobot.log.error(f'Error handling message: {e}')


async def setup(yobot: 'YoBot') -> None:
    """Loads the cog."""
    try:
        await yobot.add_cog(YoBotCoreCog(yobot))
        yobot.log.debug('YoBotCoreCog loaded.')
    except Exception as e:
        yobot.log.error(f'Error loading YoBotCoreCog: {e}')
