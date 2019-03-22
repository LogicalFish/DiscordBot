import emoji
import re

from commands.command import Command


class PollCommand(Command):

    def __init__(self):
        call = ["poll"]
        parameters = "A regular message, containing emojis marking options."
        description = "This command will react on the message using the emojis provided within it. " \
                      "This way, users can 'vote' by selecting the appropriate reaction."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        action = {"react": self.find_emojis(param),
                  "c_react": self.find_custom_emojis(param)}
        return action

    @staticmethod
    def find_emojis(message):
        """
        Find all emojis within a message.
        :param message: The message to be searched.
        :return: A list of found emojis (in emoji form)
        """
        result = re.findall(emoji.get_emoji_regexp(), message)
        return result

    @staticmethod
    def find_custom_emojis(message):
        """
        Find all custom emojis within a message.
        :param message: The message to be searched.
        :return: A list of names of found emojis.
        """
        custom = re.findall("<:(\\w+):\\d+>", message)
        return custom
