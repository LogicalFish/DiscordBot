import config
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
        self.dice_roller = StandardDiceRoller()
        super().__init__('dice_roller')
        self.parameters = self.parameters.format(configuration['dice']['dice_hardcap'],
                                                 configuration['dice']['dice_max_sides'])
        self.description = self.description.format(configuration['sign'], self.call[0])

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
        self.name = 'god_roller'
        self.call = config.localization[self.name]['commands']
        self.description = config.localization[self.name]['description'].format(configuration['sign'],
                                                                                self.call[0])
        self.dice_roller = GodRoller()


class CheatRollCommand(RollCommand):

    def __init__(self):
        super().__init__()
        self.name = 'cheat_roller'
        self.call = config.localization[self.name]['commands']
        self.description = config.localization[self.name]['description']
        self.dice_roller = CheatDice()
