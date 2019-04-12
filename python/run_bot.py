import discord
import settings
from system_manager import SystemManager
from bot_response_unit import Responder
from bot_tasks import calendar_task
from commands import run_command
from modules.reactions import reactor

# Secret Token
TOKEN = settings.TOKEN

client = discord.Client()
system = SystemManager()
bot_responder = Responder(client, system)


@client.event
async def on_ready():
    """
    Method that is called when the bot is ready.
    """
    print("The bot is ready.")
    system.bot = client.user
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
    elif message.content.startswith(settings.SIGN):
        action = run_command.run_command(message, system)
        await bot_responder.act(action, message)
    elif message.channel.id not in system.id_manager.banned_channels:
        # Switch identities based on received message.
        await bot_responder.respond(message)


@client.event
async def on_reaction_add(reaction, user):
    if not reaction.me:
        action = reactor.get_reaction_to_reaction(reaction)
        await bot_responder.act(action, reaction.message)


try:
    task = client.loop.create_task(calendar_task(client, system))
    client.run(TOKEN)
except TypeError:
    print("\nKeyboard interrupt received. Shutting down...")
    system.shutdown()
    if not client.loop.is_closed():
        task.cancel()
        client.loop.close()
    client.close()
finally:
    print("\nClient Closed. Goodbye.")
