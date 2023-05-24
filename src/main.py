import asyncio

from bot.yobot import YoBot
from utils.setup import setup_bot


def launch_bot():
    """Launches YoBot."""

    yobot = setup_bot(YoBot)
    asyncio.run(yobot.start_bot())


if __name__ == "__main__":
    launch_bot()