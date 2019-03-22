import settings
from commands.command import Command
from commands.modules import diceroll


class RollCommand(Command):

    def __init__(self):
        call = ["roll"]
        parameters = "[X]d[Y], repeated one or more times, with X being a(n optional) number between 1 and {}, " \
                     "and Y being a number between 1 and {}.".format(settings.DHARDCAP,
                                                                     settings.MAXDIETYPE)
        description = "This command will return a random output corresponding to the suggested dice. " \
                      "For example, /roll 2d6+5 results in a number between 7 (1+1+5) and 17 (6+6+5)."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        action = {}
        author = system.get_name(message.author)
        action["response"] = "{}, {}".format(author, diceroll.respond(param))
        return action
