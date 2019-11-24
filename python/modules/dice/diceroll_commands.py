from commands.command_error import CommandError
from commands.command_superclass import Command
from config import configuration
from .standard_diceroller import StandardDiceRoller
from .cheat_dice import CheatDice
from .godroll import GodRoller


class RollCommand(Command):

    """
    Command class for rolling a dice and returning the result.
    """

    def __init__(self):
        call = ["roll"]
        parameters = "[X]d[Y], repeated one or more times, with X being a(n optional) number between 2 and {}, " \
                     "and Y being a number between 2 and {}.".format(configuration['dice']['dice_hardcap'],
                                                                     configuration['dice']['dice_max_sides'])
        description = "This command will return a random output corresponding to the suggested dice. For example, " \
                      "{}{} 2d6+5 results in a number between 7 (1+1+5) and 17 (6+6+5).".format(configuration['sign'],
                                                                                                call[0])
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
                raise CommandError(str(error), configuration['dice']['dice_max_sides'])
        return action


class GodRollCommand(RollCommand):

    def __init__(self):
        super().__init__()
        self.call = ["godroll", "groll"]
        self.description = "This command will return a random output corresponding to the suggested dice, " \
                           "using the Godbound damage table. " \
                           "For example, {}{} 3d8 results in a number between 0 (0+0+0) " \
                           "and 6 (2+2+2).".format(configuration['sign'], self.call[0])
        self.dice_roller = GodRoller()


class CheatRollCommand(RollCommand):

    def __init__(self):
        super().__init__()
        self.call = ["cheatroll", "sneakyroll", "upupdowndownleftrightleftrightAB"]
        self.description = "This command will return a random, unfair output corresponding to the suggested dice."
        self.dice_roller = CheatDice()
