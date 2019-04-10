import random
import settings
import modules.dice.dicehelper as helper
from modules.dice.diceroller_superclass import DiceRoller


class StandardDiceRoller(DiceRoller):

    def format_response(self, dice_pairs, dice_results, too_many_dice):
        confirmation_response = "You have asked to roll the following dice: {}.\n".format(
            helper.dice_pairs_to_string(dice_pairs))

        error_response = ""
        if too_many_dice:
            error_response = "[ERROR]: You rolled too many dice. The list of dice was pruned. " \
                             "The maximum is {}.\n".format(settings.DHARDCAP)

        result_response = self.dice_result_to_string(dice_results)

        return confirmation_response + error_response + result_response

    def dice_result_to_string(self, dice_results):
        result_response = ""
        if len(dice_results) < settings.DSOFTCAP:
            for result in dice_results:
                if result_response:
                    result_response += "+"
                result_response += "{}".format(result)
            result_response += " = "
        result_response = "\tResult: {}**{}**.\n".format(result_response, sum(dice_results))
        return result_response

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
                    results.append(random.randint(1, y)*signbit)
            elif y == 1:
                results.append(x)
        return results
