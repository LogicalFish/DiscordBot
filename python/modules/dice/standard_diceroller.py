import random

import config
from .diceroller_superclass import DiceRoller
from . import dicehelper as helper

localization = config.localization['dice']


class StandardDiceRoller(DiceRoller):

    def format_response(self, dice_pairs, dice_results, too_many_dice):
        """
        This method returns a human-readable response to rolling a dice, confirming the dice that are rolled,
        the rolled results, and any errors.
        :param dice_pairs: The dice that have been rolled.
        :param dice_results: The results of the rolled dice.
        :param too_many_dice: Whether too many dice have been rolled.
        :return:
        """
        confirmation_response = localization['confirmation'].format(helper.dice_pairs_to_string(dice_pairs))

        error_response = ""
        if too_many_dice:
            error_response = localization['prune'].format(config.configuration['dice']['dice_hardcap'])

        result_response = self.dice_result_to_string(dice_results)

        return error_response + confirmation_response + result_response

    def dice_result_to_string(self, dice_results):
        """
        A method that takes a list of results and makes a human-readable list from them, including the final result.
        :param dice_results: A list of results from rolling dice.
        :return: A list adding up all items.
        """
        result_response = ""
        if len(dice_results) < config.configuration['dice']['dice_softcap']:
            for result in dice_results:
                if result_response:
                    result_response += "+"
                result_response += "{}".format(result)
            result_response += " = "
        result_response = localization['result'].format(result_response, sum(dice_results))
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
            if 1 < y <= config.configuration['dice']['dice_max_sides'] and \
                    len(results) <= config.configuration['dice']['dice_hardcap']:
                r = min(abs(x), config.configuration['dice']['dice_hardcap'] - len(results))
                for i in range(r):
                    results.append(self.get_random_number(1, y, signbit))
            elif y == 1:
                results.append(x)
        return results

    def get_random_number(self, min_value, max_value, sign):
        return random.randint(min_value, max_value) * sign
