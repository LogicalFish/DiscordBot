import random
from .diceroll import StandardDiceRoller


class CheatDice(StandardDiceRoller):

    """
    A class that generates a "random" number based on a list of dice-pairs.
    ('Secretly' rolls two and takes the higher, making favorable results more likely)
    """

    def get_random_number(self, min_value, max_value, sign):
        cheat_result = max(random.randint(min_value, max_value) * sign, random.randint(min_value, max_value) * sign)
        return cheat_result
