#!/usr/bin/env python3.7
import discord
import logging
from system_manager import SystemManager
from bot_response_unit import Responder
from bot_tasks import calendar_task, birthday_task, reminder_task
from commands import MainCommand
from modules.reactions import reactor
from config import configuration

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(name)-32s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# Secret Token
TOKEN = configuration['secret_token']

client = discord.Client()
system = SystemManager(configuration)
bot_responder = Responder(client, system)


@client.event
async def on_ready():
    """
    Method that is called when the bot is ready.
    """
    logger.info("The bot is ready.")
    system.bot = client.user
    # Add Bot Birthday & Nickname into any database.
    if system.database_manager:
        system.database_manager.insert_bot(system.bot)
    await bot_responder.change_visual_id()


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
    elif message.content.startswith(configuration['sign']):
        params = message.clean_content[len(configuration['sign']):]
        action = MainCommand.run_command(params, message, system)
        await bot_responder.act(action, message)
    elif message.channel.id not in system.id_manager.banned_channels:
        await bot_responder.respond(message)


@client.event
async def on_reaction_add(reaction, user):
    if not reaction.me:
        action = reactor.get_reaction_to_reaction(reaction)
        await bot_responder.act(action, reaction.message)


try:
    if configuration['commands']['calendar']:
        calendar_task = client.loop.create_task(calendar_task(client, system))
    birthday_task = client.loop.create_task(birthday_task(client, system))
    if configuration['commands']['remindme']:
        reminder_task = client.loop.create_task(reminder_task(client, system))
    client.run(TOKEN)
except TypeError:
    logger.info("\nKeyboard interrupt received. Shutting down...")
    if not client.loop.is_closed():
        calendar_task.cancel()
        birthday_task.cancel()
        reminder_task.cancel()
        client.loop.close()
    client.close()
finally:
    logger.info("\nClient Closed. Goodbye.")
