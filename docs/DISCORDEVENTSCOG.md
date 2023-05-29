# DiscordEventsCog Class

This class, `DiscordEventsCog`, represents a collection of event listeners for the `YoBot`.

It inherits from `commands.Cog` class provided by `discord.py` library.

These listeners are effectively "waiting" for specific events to occur when interacting with Discord, at which point they'll execute their associated code.

<br>

## Class Attributes

- `yobot`: Represents an instance of the `YoBot` bot class.

<br>

## Class Methods

#### `__init__(self, yobot)`

This is the constructor for the `DiscordEventsCog` class. 

It initializes an instance of the class with a reference to the bot instance (`YoBot`).

<br>

## Event Listeners

Event listeners are methods that are waiting for specific events to occur.

When those events occur, the associated method is called.

The `@commands.Cog.listener()` decorator indicates that these methods are event listeners.

The class has numerous listeners for different types of events including:

- `on_connect`: Called when YoBot connects to Discord.
- `on_ready`: Called when YoBot is ready and connected to Discord.
- `on_typing`: Called when a user starts typing.
- `on_message`: Called when a message is received.
- `on_message_edit`: Called when a message is edited.
- `on_message_delete`: Called when a message is deleted.
- `on_member_join`: Called when a member joins the server.
- `on_member_remove`: Called when a member leaves the server.
- `on_member_update`: Called when a member is updated.
- `on_guild_join`: Called when YoBot joins a guild.
- `on_guild_remove`: Called when YoBot leaves a guild.
- `on_guild_update`: Called when a guild is updated.
- `on_guild_role_create`: Called when a role is created in a guild.
- `on_guild_role_delete`: Called when a role is deleted in a guild.
- `on_guild_role_update`: Called when a role is updated in a guild.
- `on_guild_emojis_update`: Called when emojis are updated in a guild.
- `on_voice_state_update`: Called when a member's voice state is updated.
- `on_member_ban`: Called when a member is banned from a guild.
- `on_member_unban`: Called when a member is unbanned from a guild.
- `on_invite_create`: Called when an invite is created.
- `on_invite_delete`: Called when an invite is deleted.
- `on_group_join`: Called when a user joins a group DM.
- `on_group_remove`: Called when a user leaves a group DM.
- `on_relationship_add`: Called when a relationship is added.
- `on_relationship_remove`: Called when a relationship is removed.
- `on_relationship_update`: Called when a relationship is updated.
- `on_webhooks_update`: Called when webhooks are updated in a channel.
- `on_member_chunk`: Called when a chunk of members is received.
- `on_resumed`: Called when the bot resumes.
- `on_error`: Called when an error occurs.
- `on_socket_raw_receive`: Called when a raw websocket message is received.
- `on_socket_raw_send`: Called when a raw websocket message is sent.

<br>

## Function

- `async def setup(yobot: commands.Bot) -> None`

This is a standalone asynchronous function which loads the `DiscordEventsCog` into the bot instance. 

It's typically called during the bot setup process.
