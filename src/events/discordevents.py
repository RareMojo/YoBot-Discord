from discord.ext import commands

from utils.yobotlib import (get_config, log, set_avatar, set_display_name,
                            update_config_file)


class DiscordEvents(commands.Cog, name="Discord Events", description="All available Discord events."):
    def __init__(self, yobot):
        self.yobot = yobot


    @commands.Cog.listener()
    async def on_connect(self):
        """Called when YoBot connects to Discord."""
        first_run = get_config('bot').get('settings', 'first_run')
        if first_run == 'True':  
            await set_display_name(self.yobot)
            await set_avatar(self.yobot)
            update = {'settings': {'first_run': 'False'}}
            update_config_file('bot', update)

            log(msg='First run detected, set display name and avatar.')


    @commands.Cog.listener()
    async def on_ready(self):
        """Called when YoBot is ready and connected to Discord."""
        log(msg_key='setup_info', display_name=self.yobot.display_name, now_playing=self.yobot.now_playing)

        for guild in self.yobot.guilds:
            log(msg_key='link_info', display_name=self.yobot.display_name, guild=guild.name, guild_id=guild.id)

        log(msg_key='online', display_name=self.yobot.display_name)


    @commands.Cog.listener()
    async def on_message(self, message):
        """Called when a message is received."""
        if message.author == self.yobot.user:
            return

        # Example of a message handler
        if message.content.startswith('hello'):
            await message.channel.send('Hello!')


    @commands.Cog.listener()
    async def on_message_edit(before, after):
        """Called when a message is edited."""
        log(msg=f'Message edited: {before.content} -> {after.content}')


    @commands.Cog.listener()
    async def on_message_delete(message):
        """Called when a message is deleted."""
        log(msg=f'Message deleted: {message.content}')


    @commands.Cog.listener()
    async def on_member_join(member):
        """Called when a member joins the server."""
        log(msg=f'New member joined: {member.name}')


    @commands.Cog.listener()
    async def on_member_remove(member):
        """Called when a member leaves the server."""
        log(msg=f'Member left: {member.name}')


    @commands.Cog.listener()
    async def on_member_update(before, after, before_roles):
        """Called when a member is updated."""
        log(msg=f'Member updated: {before.name} -> {after.name}')


    @commands.Cog.listener()
    async def on_guild_join(guild):
        """Called when YoBot joins a new guild."""
        log(msg=f'Joined new guild: {guild.name}')


    @commands.Cog.listener()
    async def on_guild_remove(guild):
        """Called when YoBot leaves a guild."""
        log(msg=f'Left guild: {guild.name}')


    @commands.Cog.listener()
    async def on_reaction_add(reaction):
        """Called when a reaction is added to a message."""
        log(msg=f'Reaction added: {reaction.emoji}')


    @commands.Cog.listener()
    async def on_reaction_remove(reaction):
        """Called when a reaction is removed from a message."""
        log(msg=f'Reaction removed: {reaction.emoji}')


    @commands.Cog.listener()
    async def on_reaction_clear(message, reactions):
        """Called when all reactions are removed from a message."""
        log(msg=f'Reactions cleared: {len(reactions)}')


    @commands.Cog.listener()
    async def on_raw_reaction_add(payload):
        """Called when a reaction is added to a message. Includes partial data for messages not in cache."""
        log(msg=f'Reaction added: {payload.emoji}')


    @commands.Cog.listener()
    async def on_raw_reaction_remove(payload):
        """Called when a reaction is removed from a message. Includes partial data for messages not in cache."""
        log(msg=f'Reaction removed: {payload.emoji}')


    @commands.Cog.listener()
    async def on_raw_reaction_clear(payload):
        """Called when all reactions are removed from a message. Includes partial data for messages not in cache."""
        log(msg=f'Reactions cleared: {len(payload.emoji)}')


    @commands.Cog.listener()
    async def on_typing(user, channel, is_typing, latency):
        """Called when a user starts typing in a channel."""
        log(msg=f'Typing: {user.name}')


    @commands.Cog.listener()
    async def on_voice_state_update(member):
        """Called when a member's voice state changes."""
        log(msg=f'Voice state updated: {member}')


    @commands.Cog.listener()
    async def on_error(event):
        """Called when an error occurs."""
        log(msg=f'Error: {event}')


    @commands.Cog.listener()
    async def on_command_error(ctx, error):
        """Called when a command error occurs."""
        log(msg=f'Command error: {error}')


async def setup(yobot: commands.Bot) -> None:
    """Sets up the DiscordEventsCog."""
    await yobot.add_cog(DiscordEvents(yobot))