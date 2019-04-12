import discord
from discord.utils import get
import time
from bot_identity import parser
from modules.reactions import heartful


class Responder:

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
        if "response" in action:
            await message.channel.send(action["response"])
            if "board" in action and action["board"]:
                await message.channel.send(action["board"])
        if "event_embed" in action:
            embed = action["event_embed"][0]
            new_footer = embed.footer.text + self.system.nickname_manager.get_name(self.client.get_user(action["event_embed"][1]))
            embed.set_footer(text=new_footer)
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
            if self.identities.chatty and self.system.last_msg+self.identities.interval < time.time():
                await message.channel.send(parser.direct_call(self.identities.current_id, "call"))

    async def change_visual_id(self):
        """Helper function that changes the bot's nickname and game that is displayed"""
        new_nickname = self.identities.current_id.get_name()
        new_game = self.identities.current_id.get_game()
        print("Changing bot identity to {}".format(new_nickname))

        for server in self.client.guilds:
            await server.me.edit(nick=new_nickname)
            # await client.change_nickname(server.me, new_nickname)
        await self.client.change_presence(activity=discord.Game(name=new_game))

    async def respond(self, message):
        action = {}
        response, identity_switch = self.identity_response(message)
        if len(response):
            if self.identities.chatty and self.system.last_msg + self.identities.interval < time.time():
                action["response"] = response
                self.system.last_msg = time.time()
        if identity_switch:
            action["switch"] = identity_switch
        action["react"] = heartful.get_heart_in_message(message.content)
        await self.act(action, message)

    def identity_response(self, message):
        new_id = parser.find_new_id(message.content, self.identities.identities)
        if len(new_id) and self.identities.current_id not in new_id:
            identity_switch = new_id[0]
            response = parser.direct_call(identity_switch, "call")
        else:
            identity_switch = False
            response = parser.get_response(message.content, self.identities.current_id)
        return response, identity_switch
