import random
import settings
from commands.modules.dice.diceroll import StandardDiceRoller


class CheatDice(StandardDiceRoller):

    def roll_the_dice(self, dice_pairs):
        """
        A method that generates a random number based on a list of dice-pairs.
        :param dice_pairs: A list of tuples, each tuple having a length of two and representing dice notation.
        :return: A list containing a random number for each dice in the dice_pairs list.
        """
        results = []
        for pair in dice_pairs:
            x, y = pair
            signbit = -1 if x < 0 else 1
            if 1 < y <= settings.MAXDIETYPE and len(results) <= settings.DHARDCAP:
                r = min(abs(x), settings.DHARDCAP - len(results))
                for i in range(r):
                    cheat_result = max(random.randint(1, y)*signbit, random.randint(1, y)*signbit)
                    results.append(cheat_result)
            elif y == 1:
                results.append(x)
        return results
