from discord.ext import commands


class DiscordCommandsCog(commands.Cog, name="Discord Commands", description="All available Discord commands."):
  def __init__(self, yobot: commands.Bot) -> None:
    self.yobot: commands.Bot = yobot


  @commands.hybrid_command(name="ping")
  async def ping_command(self, ctx: commands.Context) -> None:
    """
    PING
    """

    await ctx.send("PONG!")
    # we use ctx.send and this will handle both the message command and app command of sending.
    # added note: you can check if this command is invoked as an app command by checking the `ctx.interaction` attribute.
    

  @commands.hybrid_group(name="parent")
  async def parent_command(self, ctx: commands.Context) -> None:
    """
    We even have the use of parents.
    """
    ...   # nothing we want to do in here, I guess!
    

  @parent_command.command(name="sub")
  async def sub_command(self, ctx: commands.Context, argument: str) -> None:
    """
    This subcommand can now be invoked with `?parent sub <arg>` or `/parent sub <arg>` (once synced).
    """

    await ctx.send(f"Hello, you sent {argument}!")
    
    
async def setup(yobot: commands.Bot) -> None:
  """Loads the cog."""
  await yobot.add_cog(DiscordCommandsCog(yobot))