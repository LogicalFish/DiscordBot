import random

from config import configuration
from .standard_diceroller import StandardDiceRoller


class GodRoller(StandardDiceRoller):

    def dice_result_to_string(self, dice_results):
        result_response = ""
        if len(dice_results) < configuration['dice']['dice_softcap']:
            for result in dice_results:
                if result_response:
                    result_response += "+"
                if result[2]:
                    composite = "{}+{}".format(result[1], result[2])
                else:
                    composite = result[1]
                result_response += " {}*({})* ".format(result[0], composite)
            result_response += " = "
        dice_sum = sum(result[0] for result in dice_results)
        result_response = "\tResult: {}**{}**.\n".format(result_response, dice_sum)
        return result_response

    def roll_the_dice(self, dice_pairs):
        """
        A method that generates a random number based on a list of dice-pairs.
        :param dice_pairs: A list of tuples, each tuple having a length of two and representing dice notation.
        :return: A list containing a random number for each dice in the dice_pairs list.
        """
        results = []
        modifier = self.get_modifier(dice_pairs)
        for pair in dice_pairs:
            x, y = pair
            signbit = -1 if x < 0 else 1
            if 1 < y <= configuration['dice']['dice_max_sides'] and len(results) <= configuration['dice']['dice_hardcap']:
                amount = min(abs(x), configuration['dice']['dice_hardcap'] - len(results))
                for i in range(amount):
                    straight_roll = random.randint(1, y)*signbit
                    final_number = self.translate_number(straight_roll + modifier)
                    results.append((final_number, straight_roll, modifier))
        return results

    @staticmethod
    def get_modifier(dice_pairs):
        modifier = 0
        for x, y in dice_pairs:
            if y == 1:
                modifier += x
        return modifier

    @staticmethod
    def translate_number(number):
        if number < 2:
            return 0
        if number < 6:
            return 1
        if number < 10:
            return 2
        return 4
