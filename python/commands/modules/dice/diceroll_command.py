import settings
from commands.command_superclass import Command
from commands.modules.dice.diceroll import StandardDiceRoller


class RollCommand(Command):

    def __init__(self):
        call = ["roll"]
        parameters = "[X]d[Y], repeated one or more times, with X being a(n optional) number between 1 and {}, " \
                     "and Y being a number between 1 and {}.".format(settings.DHARDCAP,
                                                                     settings.MAXDIETYPE)
        description = "This command will return a random output corresponding to the suggested dice. " \
                      "For example, /{} 2d6+5 results in a number between 7 (1+1+5) and 17 (6+6+5).".format(call[0])
        self.dice_roller = StandardDiceRoller()
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        author = system.nickname_manager.get_name(message.author)
        action = {"response": "{}, ".format(author)}

        parallel_list = param.split("|")
        for parallel_input in parallel_list:
            action["response"] += self.dice_roller.main_dice_method(parallel_input)
        return action
