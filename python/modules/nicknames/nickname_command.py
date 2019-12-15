import random

import config
from commands.command_superclass import Command


class CallmeCommand(Command):

    """
    Command class for adding a nickname for the caller.
    """

    def __init__(self):
        super().__init__('nicknames')
        self.parameters = self.parameters.format(config.configuration['nicknames']['max_length'])

    def execute(self, param, message, system):
        if len(param):
            system.nickname_manager.add_nickname(message.author.id,
                                                 param[:config.configuration['nicknames']['max_length']])
        else:
            system.nickname_manager.add_nickname(message.author.id, self.get_default_name())
        return {"response": config.localization[self.name]['response'].format(system.nickname_manager.get_name(message.author))}

    @staticmethod
    def get_default_name():
        """
        Helper method for getting a 'default' name in case a user forgets to actually submit one.
        :return: A random 'default' name.
        """
        return random.choice(config.configuration['nicknames']['default_nicknames'])
