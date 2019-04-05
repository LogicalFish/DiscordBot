import discord
from discord.utils import get
import asyncio
import time
import settings
from system_manager import SystemManager
from commands import run_command
from responder import parser

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
                await client.send_message(message.channel, parser.direct_call(identities.current_id, "call"))
        elif identities.chatty and system.last_msg+identities.interval < time.time():
            # Respond to distinct phrases based on identity.
            response = parser.get_response(message.content, identities.current_id)
            if len(response):
                await client.send_message(message.channel, response)
                system.last_msg = time.time()


async def act(action, message):
    """
    Method that acts in response to an action dictionary.
    :param action: The action dictionary, as detailed in run_command.py
    :param message: The original message the dictionary was based on.
    """
    if "response" in action:
        response = action["response"].replace("[ERROR]:", parser.direct_call(identities.current_id, "error"))
        await client.send_message(message.channel, response)
        if "board" in action and action["board"]:
            await client.send_message(message.channel, action["board"])
    if "react" in action:
        for emoji in action["react"]:
            await client.add_reaction(message, emoji)
    if "c_react" in action:
        for custom_emoji in action["c_react"]:
            await client.add_reaction(message, get(client.get_all_emojis(), name=custom_emoji))
    if "leave" in action:
        if identities.chatty and system.last_msg+identities.interval < time.time():
            await client.send_message(message.channel, parser.direct_call(identities.current_id, "leave"))
        identities.current_id = action["leave"]
        await change_visual_id()
        if identities.chatty and system.last_msg+identities.interval < time.time():
            await client.send_message(message.channel, parser.direct_call(identities.current_id, "call"))


async def change_visual_id():
    """Helper function that changes the bot's nickname and game that is displayed"""
    name_str = identities.current_id.get_name()
    game_str = identities.current_id.get_game()
    print("Changing responder to {}".format(name_str))

    for server in client.servers:
        await client.change_nickname(server.me, name_str)
    await client.change_presence(game=discord.Game(name=game_str))


async def calendar_task():
    """
    A separate thread, keeping track of tasks on the calendar.
    """
    await client.wait_until_ready()

    while not client.is_closed:
        reminders = system.time_manager.clock_pass()
        for date, reminder_message, channel_name, tag_name in reminders:
            if len(channel_name):
                channel = get(client.get_all_channels(), name=channel_name)
                tag = get(channel.server.roles, name=tag_name)
                if tag:
                    reminder_message = "Reminder for {}! {}".format(tag.mention, reminder_message)
                if channel:
                    await client.send_message(channel, reminder_message)
        await asyncio.sleep(30)


client.loop.create_task(calendar_task())

client.run(TOKEN)
