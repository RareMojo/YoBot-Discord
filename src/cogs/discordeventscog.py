import discord.ext.commands as commands
from utils.yobot_lib import update_yobot, welcome_to_yobot

class DiscordEventsCog(commands.Cog):
    """Discord events for YoBot to listen to."""
    def __init__(self, yobot):
        self.yobot = yobot


    @commands.Cog.listener()
    async def on_connect(self):
        """Called when YoBot connects to Discord."""
        await update_yobot(self.yobot) # Update YoBot's status and activity, if applicable.
        

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when YoBot is ready and connected to Discord."""
        await welcome_to_yobot(self.yobot) # Send a welcome message to the console.
            
            
    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        """Called when a user starts typing. """
        
        #log(f'{user} started typing in {channel} at {when}') ##This is very spammy, so it's commented out by default.
            

    @commands.Cog.listener()
    async def on_message(self, message):
        """Called when a message is received."""
        if message.author == self.yobot.user: # Ignore messages from the bot itself
            return
        
        #log(f'Message by {message.author} in {message.channel}: {message.content}') ## This is very spammy, so it's commented out by default.

        # Example of a message handler
        if message.content.startswith('hello'):
            await message.channel.send('Hello!')


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Called when a message is edited."""
        self.yobot.log.info(f'Message edited: {before.content} -> {after.content}')


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Called when a message is deleted."""
        self.yobot.log.info(f'Message deleted: {message}')


    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Called when a member joins the server."""
        self.yobot.log.info(f'New member joined: {member}')


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Called when a member leaves the server."""
        self.yobot.log.info(f'Member left: {member}')
        
        
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Called when a member is updated."""
        self.yobot.log.info(f'Member updated: {before} -> {after}')
    
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Called when YoBot joins a guild."""
        self.yobot.log.info(f'Joined guild: {guild}')
    
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """Called when YoBot leaves a guild."""
        self.yobot.log.info(f'Left guild: {guild}')
    
    
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        """Called when a guild is updated."""
        self.yobot.log.info(f'Guild updated: {before} -> {after}')
        
        
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        """Called when a role is created in a guild."""
        self.yobot.log.info(f'Role created: {role}')
        
        
    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        """Called when a role is deleted in a guild."""
        self.yobot.log.info(f'Role deleted: {role}')
    
    
    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        """Called when a role is updated in a guild."""
        self.yobot.log.info(f'Role updated: {before} -> {after}')
    
    
    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        """Called when emojis are updated in a guild."""
        self.yobot.log.info(f'Emojis updated: {before} -> {after}')


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Called when a member's voice state is updated."""
        self.yobot.log.info(f'Voice state updated: {before} -> {after}')


    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        """Called when a member is banned from a guild."""
        self.yobot.log.info(f'Member banned: {user}')


    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        """Called when a member is unbanned from a guild."""
        self.yobot.log.info(f'Member unbanned: {user}')


    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        """Called when an invite is created."""
        self.yobot.log.info(f'Invite created: {invite}')


    @commands.Cog.listener()
    async def on_invite_delete(self, invite):    
        """Called when an invite is deleted."""
        self.yobot.log.info(f'Invite deleted: {invite}')
        
        
    @commands.Cog.listener()
    async def on_group_join(self, channel, user):
        """Called when a user joins a group DM."""
        self.yobot.log.info(f'User {user} joined group DM {channel}')
        
        
    @commands.Cog.listener()
    async def on_group_remove(self, channel, user):
        """Called when a user leaves a group DM."""
        self.yobot.log.info(f'User {user} left group DM {channel}')


    @commands.Cog.listener()
    async def on_relationship_add(self, relationship):
        """Called when a relationship is added."""
        self.yobot.log.info(f'Relationship added: {relationship}')
    
    
    @commands.Cog.listener()
    async def on_relationship_remove(self, relationship):
        """Called when a relationship is removed."""
        self.yobot.log.info(f'Relationship removed: {relationship}')


    @commands.Cog.listener()
    async def on_relationship_update(self, before, after):
        """Called when a relationship is updated."""
        self.yobot.log.info(f'Relationship updated: {before} -> {after}')


    @commands.Cog.listener()
    async def on_webhooks_update(self, channel):
        """Called when webhooks are updated in a channel."""
        self.yobot.log.info(f'Webhooks updated: {channel}')


    @commands.Cog.listener()
    async def on_member_chunk(self, members):
        """Called when a chunk of members is received."""
        self.yobot.log.info(f'Member chunk received: {members}')


    @commands.Cog.listener()
    async def on_resumed(self):
        """Called when the bot resumes."""
        self.yobot.log.info('Resumed')


    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        """Called when an error occurs."""
        self.yobot.log.info(f'Error in {event}: {args[0]}')


    @commands.Cog.listener()
    async def on_socket_raw_receive(self, msg):
        """Called when a raw websocket message is received."""
        self.yobot.log.info(f'Socket raw receive: {msg}')


    @commands.Cog.listener()
    async def on_socket_raw_send(self, payload):
        """Called when a raw websocket message is sent."""
        self.yobot.log.info(f'Socket raw send: {payload}')


async def setup(yobot: commands.Bot) -> None:
  """Loads the cog."""
  await yobot.add_cog(DiscordEventsCog(yobot))