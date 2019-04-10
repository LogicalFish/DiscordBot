from modules.dice.diceroll_command import RollCommand
from modules.dice.cheat_dice import CheatDice


class CheatRollCommand(RollCommand):

    def __init__(self):
        super().__init__()
        self.call = ["cheatroll", "sneakyroll", "upupdowndownleftrightleftrightAB"]
        self.description = "This command will return a random, unfair output corresponding to the suggested dice."
        self.dice_roller = CheatDice()
