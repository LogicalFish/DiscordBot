import discord
from discord.utils import get
import time
from bot_identity import parser
from modules.reactions import reactor


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
            user_from_id = self.system.nickname_manager.get_name_by_id(action["add_id"], self.client, message.guild)
            if "response" in action:
                action["response"].format(user_from_id)
            if "embed" in action:
                new_footer = action["embed"].footer.text + user_from_id
                action["embed"].set_footer(text=new_footer)
        if "response" in action:
            await message.channel.send(action["response"])
            if "board" in action and action["board"]:
                await message.channel.send(action["board"])
            if "scores" in action and action["scores"]:
                await message.channel.send(action["scores"])
        if "embed" in action:
            embed = action["embed"]
            await message.channel.send(embed=embed)
        if "react" in action:
            for emoji in action["react"]:
                await message.add_reaction(emoji)
        if "c_react" in action:
            for custom_emoji in action["c_react"]:
                await message.add_reaction(get(self.client.emojis, name=custom_emoji))
        if "leave" in action:
            if self.identities.chatty and self.system.last_msg+self.identities.interval < time.time():
                await message.channel.send(parser.direct_call(self.identities.current_id, "leave"))
            self.identities.current_id = action["leave"]
            await self.change_visual_id()
            await message.channel.send(parser.direct_call(self.identities.current_id, "call"))

    async def change_visual_id(self):
        """
        Helper function that changes the bot's nickname and game that is displayed
        """
        new_nickname = self.identities.current_id.get_name()
        new_game = self.identities.current_id.get_game()
        print("Changing bot identity to {}".format(new_nickname))

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
        if len(response):
            if self.identities.chatty and self.system.last_msg + self.identities.interval < time.time():
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
        new_id = parser.find_new_id(message.content, self.identities.identities)
        if len(new_id) and self.identities.current_id not in new_id:
            identity_switch = new_id[0]
            response = parser.direct_call(identity_switch, "call")
        else:
            identity_switch = False
            response = parser.get_response(message.content, self.identities.current_id)
        return response, identity_switch
