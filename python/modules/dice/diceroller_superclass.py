import settings
import modules.dice.dicehelper as helper


class DiceRoller:

    def main_dice_method(self, message):
        dice_pairs = helper.string_to_dice_pairs(message)
        dice_amount = helper.get_dice_count(dice_pairs)
        helper.sort_dice(dice_pairs)
        dice_pairs = helper.prune_dice(dice_pairs)
        if len(dice_pairs) > 0:
            results = self.roll_the_dice(dice_pairs)
            too_many_dice = dice_amount > settings.DHARDCAP
            message = self.format_response(dice_pairs, results, too_many_dice)
            return message
        else:
            raise ValueError("invalid_dice")

    def format_response(self, dice_pairs, results, too_many_dice):
        raise NotImplementedError

    def roll_the_dice(self, dice_pairs):
        raise NotImplementedError
