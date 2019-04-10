from modules.dice.diceroll_command import RollCommand
from modules.dice.godroll import GodRoller


class GodRollCommand(RollCommand):

    def __init__(self):
        super().__init__()
        self.call = ["godroll", "groll"]
        self.description = "This command will return a random output corresponding to the suggested dice, " \
                           "using the Godbound damage table. " \
                           "For example, /{} 3d8 results in a number between 0 (0+0+0) " \
                           "and 6 (2+2+2).".format(self.call[0])
        self.dice_roller = GodRoller()
