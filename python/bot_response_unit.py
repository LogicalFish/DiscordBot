import discord
from discord.utils import get
import time
from modules.reactions import reactor
import logging

logger = logging.getLogger(__name__)


class Responder:

    """
    A class whose main job it is to response to messages sent by client.
    """

    def __init__(self, client, system):
        self.client = client
        self.system = system
        self.identities = self.system.id_manager

    async def act(self, action, message):
        """
        Method that acts in response to an action dictionary.
        :param action: The action dictionary, as detailed in run_command.py
        :param message: The original message the dictionary was based on.
        """
        if "switch" in action:
            self.identities.current_id = action["switch"]
            await self.change_visual_id()
        if "add_id" in action:
            user_from_id = await self.system.get_user_by_id(action["add_id"], client=self.client, guild=message.guild)
            user_name = self.system.name_manager.get_name(user_from_id)
            if "response" in action:
                action["response"].format(user_name)
            if "embed" in action:
                new_footer = action["embed"].footer.text + user_name
                action["embed"].set_footer(text=new_footer)
        if "response" in action:
            logging.debug("Sending message: {}".format(action["response"]))
            await message.channel.send(action["response"])
            if "board" in action and action["board"]:
                logging.debug("Attaching board to message.")
                await message.channel.send(action["board"])
            if "scores" in action and action["scores"]:
                logging.debug("Attaching scores to message.")
                await message.channel.send(action["scores"])
        if "embed" in action:
            logging.debug("Sending Embed.")
            embed = action["embed"]
            await message.channel.send(embed=embed)
        if "react" in action:
            for emoji in action["react"]:
                logging.debug("Adding the following reaction: {}.".format(emoji))
                await message.add_reaction(emoji)
        if "c_react" in action:
            for custom_emoji in action["c_react"]:
                logging.debug("Adding the following reaction: {}.".format(custom_emoji))
                await message.add_reaction(get(self.client.emojis, name=custom_emoji))
        if "leave" in action:
            if self.identities.verbose and self.system.last_msg+self.identities.interval < time.time():
                await message.channel.send(self.identities.id_statement("general", "leave"))
            self.identities.current_id = action["leave"]
            await self.change_visual_id()
            await message.channel.send(self.identities.id_statement("general", "call"))

    async def change_visual_id(self):
        """
        Helper function that changes the bot's nickname and game that is displayed
        """
        new_nickname = self.identities.current_id.name
        new_game = self.identities.current_id.get_game()
        logger.info("Changing bot identity to {}".format(new_nickname))

        for server in self.client.guilds:
            await server.me.edit(nick=new_nickname)
        await self.client.change_presence(activity=discord.Game(name=new_game))

    async def respond(self, message):
        """
        Method that responds to a message that is not a command.
        :param message: The message that should be responded to.
        """
        action = {}
        response, identity_switch = self.identity_response(message)
        if response:
            if self.identities.verbose and self.system.last_msg + self.identities.interval < time.time():
                action["response"] = response
                self.system.last_msg = time.time()
        if identity_switch:
            action["switch"] = identity_switch
        action["react"], action["c_react"] = reactor.get_reaction_to_message(message)
        await self.act(action, message)

    def identity_response(self, message):
        """
        Method that gets a response from an identity.
        :param message: The message which should be responded to.
        :return: A string containing a response &
                A new identity (or false if the identity should not change).
        """
        new_id = self.identities.find_new_id(message.content)
        if len(new_id) and self.identities.current_id not in new_id:
            identity_switch = new_id[0]
            response = identity_switch.get_phrase("general", "call")
        else:
            identity_switch = False
            response = self.identities.get_identity_response(message)
        return response, identity_switch
