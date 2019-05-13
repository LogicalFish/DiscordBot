import random
from . import nickname_config as config
from commands.command_superclass import Command


class CallmeCommand(Command):

    """
    Command class for adding a nickname for the caller.
    """

    def __init__(self):
        call = ["callme"]
        parameters = "The new nickname, up to {} letters long.".format(config.MAX_NICK_NAME)
        description = "This command will change the name the bot uses to refer to you. " \
                      "It will not change server nicknames or settings."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        if len(param):
            system.nickname_manager.add_nickname(message.author.id, param[:config.MAX_NICK_NAME])
        else:
            system.nickname_manager.add_nickname(message.author.id, self.get_default_name())
        return {"response": "Vanaf dit moment noem ik je {}".format(system.nickname_manager.get_name(message.author))}

    @staticmethod
    def get_default_name():
        """
        Helper method for getting a 'default' name in case a user forgets to actually submit one.
        :return: A random 'default' name.
        """
        return random.choice(config.DEFAULT_NICKNAMES)
