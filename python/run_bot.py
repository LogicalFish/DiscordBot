import discord
from discord.utils import get
import asyncio
import time
import settings
from system_manager import SystemManager
from commands import run_command
from bot_identity import parser

# Secret Token
TOKEN = settings.TOKEN

client = discord.Client()
system = SystemManager()
identities = system.id_manager


@client.event
async def on_ready():
    """
    Method that is called when the bot is ready.
    """
    print("The bot is ready.")
    system.bot = client.user
    await change_visual_id()


@client.event
async def on_message(message):
    """
    Method that is called when a message is received.
    Depending on the contents of the message, a response may be sent, or the state of the bot may change.
    :param message: The message object that is received.
    """
    if message.author == client.user:
        # The bot should not respond to its own messages.
        return
    elif message.content.startswith(settings.SIGN):
        action = run_command.run_command(message, system)
        await act(action, message)
    elif message.channel.id not in identities.banned_channels:
        # Switch identities based on received message.
        new_id = parser.find_new_id(message.content, identities.identities)
        if len(new_id) and identities.current_id not in new_id:
            identities.current_id = new_id[0]
            await change_visual_id()
            if identities.chatty and system.last_msg+identities.interval < time.time():
                await message.channel.send(parser.direct_call(identities.current_id, "call"))
        elif identities.chatty and system.last_msg+identities.interval < time.time():
            # Respond to distinct phrases based on identity.
            response = parser.get_response(message.content, identities.current_id)
            if len(response):
                await message.channel.send(response)
                system.last_msg = time.time()


async def act(action, message):
    """
    Method that acts in response to an action dictionary.
    :param action: The action dictionary, as detailed in run_command.py
    :param message: The original message the dictionary was based on.
    """
    if "response" in action:
        await message.channel.send(action["response"])
        if "board" in action and action["board"]:
            await message.channel.send(action["board"])
    if "react" in action:
        for emoji in action["react"]:
            await message.add_reaction(emoji)
    if "c_react" in action:
        for custom_emoji in action["c_react"]:
            await message.add_reaction(get(client.emojis, name=custom_emoji))
    if "leave" in action:
        if identities.chatty and system.last_msg+identities.interval < time.time():
            await message.channel.send(parser.direct_call(identities.current_id, "leave"))
        identities.current_id = action["leave"]
        await change_visual_id()
        if identities.chatty and system.last_msg+identities.interval < time.time():
            await message.channel.send(parser.direct_call(identities.current_id, "call"))


async def change_visual_id():
    """Helper function that changes the bot's nickname and game that is displayed"""
    new_nickname = identities.current_id.get_name()
    new_game = identities.current_id.get_game()
    print("Changing bot identity to {}".format(new_nickname))

    for server in client.guilds:
        await server.me.edit(nick=new_nickname)
        # await client.change_nickname(server.me, new_nickname)
    await client.change_presence(activity=discord.Game(name=new_game))


async def calendar_task():
    """
    A separate thread, keeping track of tasks on the calendar.
    """
    await client.wait_until_ready()
    while not client.is_closed():
        reminders = system.time_manager.clock_pass()
        for date, reminder_message, channel_name, tag_name in reminders:
            if len(channel_name):
                channels = filter(lambda ch: ch.name == channel_name, client.get_all_channels())
                for channel in channels:
                    if isinstance(channel, discord.TextChannel):
                        tag = get(channel.guild.roles, name=tag_name)
                        if tag:
                            new_message = "Reminder for {}! {}".format(tag.mention, reminder_message)
                        else:
                            new_message = reminder_message
                        await channel.send(new_message)
        await asyncio.sleep(30)


try:
    task = client.loop.create_task(calendar_task())
    client.run(TOKEN)
except TypeError:
    print("\nKeyboard interrupt received. Shutting down...")
    system.shutdown()
    if not client.loop.is_closed():
        task.cancel()
        client.loop.close()
    client.close()
finally:
    print("Client Closed. Goodbye.")
