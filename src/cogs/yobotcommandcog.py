from typing import TYPE_CHECKING

from discord.ext import commands

if TYPE_CHECKING:
    from bot.yobot import YoBot


class YoBotCommandCog(commands.Cog, name="YoBot Discord Commands", description="All available Discord commands."):
    """Discord commands for YoBot to execute.

    Attributes:
      yobot (YoBot): The bot instance.
    """

    def __init__(self: 'YoBotCommandCog', yobot: 'YoBot'):
        self.yobot = yobot

    @commands.hybrid_command(name="ping")
    async def ping_command(self, ctx: commands.Context) -> None:
        """PING! command example"""
        try:
            await ctx.send("Pong!")  # Example of a simple command.
        except Exception as e:
            self.yobot.log.error(f"Error in ping_command: {e}")
            await ctx.send("An error occurred while executing the command.")

    @commands.hybrid_command(name="admin")
    async def admin_command(self, ctx: commands.Context) -> None:
        """Admin only command example"""
        allowed_roles = ["Admin", "Moderator"]
        if any(role.name in allowed_roles for role in ctx.author.roles):  # type: ignore
            try:
                await ctx.send("Admin!")
            except Exception as e:
                self.yobot.log.error(f"Error in admin_command: {e}")
                await ctx.send("An error occurred while executing the command.")
        else:
            try:
                await ctx.send("You don't have permission to use this command.")
            except Exception as e:
                self.yobot.log.error(f"Error in admin_command: {e}")
            self.yobot.log.warning(
                f"{ctx.author} tried to use the ping command.")

    @commands.command(name="restart")
    async def restart(self, ctx):
        """Restarts the bot."""
        try:
            await ctx.send('Restarting...')
            self.yobot.stop_bot()
            await self.yobot.start_bot()
        except Exception as e:
            self.yobot.log.error(f"Error in restart command: {e}")
            await ctx.send("An error occurred while executing the command.")

    @commands.hybrid_group(name="parent")
    async def parent_command(self, ctx: commands.Context) -> None:
        """ This is a parent command. It looks like this: /parent <subcommand>"""
        if ctx.invoked_subcommand is None:
            try:
                await ctx.send("Invalid subcommand passed...")
            except Exception as e:
                self.yobot.log.error(f"Error in parent_command: {e}")

    @parent_command.command(name="sub")
    async def sub_command(self, ctx: commands.Context, argument: str) -> None:
        """This is a sub command. It looks like this: /parent sub <argument>"""
        try:
            await ctx.send(f"Argument passed: {argument}")
        except Exception as e:
            self.yobot.log.error(f"Error in sub_command: {e}")
            await ctx.send("An error occurred while executing the command.")


async def setup(yobot: 'YoBot') -> None:
    """Loads the cog."""
    try:
        await yobot.add_cog(YoBotCommandCog(yobot))
        yobot.log.debug("YoBotCommandCog loaded.")
    except Exception as e:
        yobot.log.error(f"Error loading YoBotCommandCog: {e}")
