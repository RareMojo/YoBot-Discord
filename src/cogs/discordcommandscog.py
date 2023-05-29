from discord.ext import commands


class DiscordCommandsCog(commands.Cog, name="Discord Commands", description="All available Discord commands."):
  """Discord commands for YoBot to execute.

  Args:
    commands.Cog (commands.Cog): The base class that all cogs must inherit from.
    name (str, optional): The name of the cog. Defaults to "Discord Commands".
    description (str, optional): The description of the cog. Defaults to "All available Discord commands.".
  """
  def __init__(self, yobot):
    self.yobot = yobot


  @commands.hybrid_command(name="ping")
  async def ping_command(self, ctx: commands.Context) -> None:
      """PING! command example"""
      await ctx.send("Pong!") # Example of a simple command.


  @commands.hybrid_command(name="admin")
  async def admin_command(self, ctx: commands.Context) -> None:
      """Admin only command example"""
      allowed_roles = ["Admin", "Moderator"]
      if any(role.name in allowed_roles for role in ctx.author.roles): # type: ignore
          await ctx.send("Admin!")
      else:
          await ctx.send("You don't have permission to use this command.")
          self.yobot.log.warning(f"{ctx.author} tried to use the ping command.")


  @commands.command(name="restart")
  async def restart(self, ctx):
      """Restarts the bot."""
      await ctx.send('Restarting...')
      self.yobot.stop_bot()
      await self.yobot.start_bot() 


  @commands.hybrid_group(name="parent")
  async def parent_command(self, ctx: commands.Context) -> None:
    """ This is a parent command. It looks like this: /parent <subcommand>"""
    if ctx.invoked_subcommand is None:
      await ctx.send("Invalid subcommand passed...")
    

  @parent_command.command(name="sub")
  async def sub_command(self, ctx: commands.Context, argument: str) -> None:
    """This is a sub command. It looks like this: /parent sub <argument>"""
    await ctx.send(f"Argument passed: {argument}")
    
    
async def setup(yobot: commands.Bot) -> None:
  """Loads the cog."""
  await yobot.add_cog(DiscordCommandsCog(yobot))