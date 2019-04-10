import random
import settings
from commands.command_superclass import Command


class CallmeCommand(Command):

    def __init__(self):
        call = ["callme"]
        parameters = "The new nickname, up to {} letters long.".format(settings.MAX_NICK_NAME)
        description = "This command will change the name the bot uses to refer to you. " \
                      "It will not change server nicknames or settings."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        if len(param):
            system.nickname_manager.add_nickname(message.author.id, param[:settings.MAX_NICK_NAME])
        else:
            system.nickname_manager.add_nickname(message.author.id, self.get_default_name())
        return {"response": "Vanaf dit moment noem ik je {}".format(system.nickname_manager.get_name(message.author))}

    @staticmethod
    def get_default_name():
        return random.choice(["The Void", "Ishmael", "maybe", "Spartacus"])