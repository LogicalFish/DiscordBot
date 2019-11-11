from commands.command_error import CommandError
from commands.command_superclass import Command
from .diceroll import StandardDiceRoller
from . import dice_config as config


class RollCommand(Command):

    """
    Command class for rolling a dice and returning the result.
    """

    def __init__(self):
        call = ["roll"]
        parameters = "[X]d[Y], repeated one or more times, with X being a(n optional) number between 2 and {}, " \
                     "and Y being a number between 2 and {}.".format(config.DHARDCAP,
                                                                     config.MAXDIETYPE)
        description = "This command will return a random output corresponding to the suggested dice. " \
                      "For example, /{} 2d6+5 results in a number between 7 (1+1+5) and 17 (6+6+5).".format(call[0])
        self.dice_roller = StandardDiceRoller()
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        author = system.nickname_manager.get_name(message.author)
        action = {"response": "{}, ".format(author)}

        parallel_list = param.split("|")
        for parallel_input in parallel_list:
            try:
                action["response"] += self.dice_roller.main_dice_method(parallel_input)
            except ValueError as error:
                raise CommandError(str(error), None)
        return action
