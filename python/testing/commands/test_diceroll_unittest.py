import unittest

from modules.dice import diceroll
import settings


class TestDiceRoll(unittest.TestCase):

    # TESTS FOR diceroll.string_to_dice_pairs(msg)

    def test_string_to_dice_pairs_simple(self):
        test_input = "4d6"
        outcome = diceroll.string_to_dice_pairs(test_input)
        expected_outcome = [(4, 6)]
        self.assertEqual(outcome, expected_outcome, "{} should output {}".format(test_input, expected_outcome))

    def test_string_to_dice_pairs_multiple(self):
        test_input = "6d6 + 1d8 + 5d4"
        outcome = diceroll.string_to_dice_pairs(test_input)
        expected_outcome = [(6, 6), (1, 8), (5, 4)]
        self.assertEqual(outcome, expected_outcome, "{} should output {}".format(test_input, expected_outcome))

    def test_string_to_dice_pairs_single(self):
        test_input = "d20"
        outcome = diceroll.string_to_dice_pairs(test_input)
        expected_outcome = [(1, 20)]
        self.assertEqual(outcome, expected_outcome, "{} should output {}".format(test_input, expected_outcome))

    def test_string_to_dice_pairs_lone_integer(self):
        test_input = "1d20+5"
        outcome = diceroll.string_to_dice_pairs(test_input)
        expected_outcome = [(1, 20), (5, 1)]
        self.assertEqual(outcome, expected_outcome, "{} should output {}".format(test_input, expected_outcome))

    def test_string_to_dice_pairs_negative(self):
        test_input = "- 1d8 - 1d6 - 5"
        outcome = diceroll.string_to_dice_pairs(test_input)
        expected_outcome = [(-1, 8), (-1, 6), (-5, 1)]
        self.assertEqual(outcome, expected_outcome, "{} should output {}".format(test_input, expected_outcome))

    def test_string_to_dice_pairs_max_dietype(self):
        test_input = "2d{}+1d20".format(settings.MAXDIETYPE+1)
        outcome = diceroll.string_to_dice_pairs(test_input)
        expected_outcome = [(1, 20)]
        self.assertEqual(outcome, expected_outcome, "{} should output {}".format(test_input, expected_outcome))

    def test_string_to_dice_pairs_empty(self):
        test_input = "___"
        outcome = diceroll.string_to_dice_pairs(test_input)
        expected_outcome = []
        self.assertEqual(outcome, expected_outcome, "{} should output {}".format(test_input, expected_outcome))

    # TESTS FOR diceroll.dice_pairs_to_string(dice_pairs)

    def test_dice_pairs_to_string_simple(self):
        test_input = [(4, 6)]
        outcome = diceroll.dice_pairs_to_string(test_input)
        expected_outcome = "4d6"
        self.assertEqual(outcome, expected_outcome, "{} should output {}".format(test_input, expected_outcome))

    def test_dice_pairs_to_string_multiple(self):
        test_input = [(6, 6), (1, 8), (5, 4)]
        outcome = diceroll.dice_pairs_to_string(test_input)
        expected_outcome = "6d6+1d8+5d4"
        self.assertEqual(outcome, expected_outcome, "{} should output {}".format(test_input, expected_outcome))

    def test_dice_pairs_to_string_lone_integer(self):
        test_input = [(1, 20), (5, 1)]
        outcome = diceroll.dice_pairs_to_string(test_input)
        expected_outcome = "1d20+5"
        self.assertEqual(outcome, expected_outcome, "{} should output {}".format(test_input, expected_outcome))

    def test_dice_pairs_to_string_empty(self):
        test_input = []
        outcome = diceroll.dice_pairs_to_string(test_input)
        expected_outcome = ""
        self.assertEqual(outcome, expected_outcome, "{} should output {}".format(test_input, expected_outcome))

    def test_string_to_dice_pairs_to_string_simple(self):
        test_input = "1d20+3d6+5"
        interim_value = diceroll.string_to_dice_pairs(test_input)
        expected_interim = [(1, 20), (3, 6), (5, 1)]
        self.assertEqual(interim_value, expected_interim, "{} should lead to {}".format(test_input, expected_interim))
        outcome = diceroll.dice_pairs_to_string(interim_value)
        expected_outcome = "1d20+3d6+5"
        self.assertEqual(outcome, expected_outcome, "Input should be the same as the output.")

    def test_string_to_dice_pairs_to_string_complex(self):
        test_input = "This is a test: 1d20 + abcd + 3d6 + b + 5"
        interim_value = diceroll.string_to_dice_pairs(test_input)
        expected_interim = [(1, 20), (3, 6), (5, 1)]
        self.assertEqual(interim_value, expected_interim, "{} should lead to {}".format(test_input, expected_interim))
        outcome = diceroll.dice_pairs_to_string(interim_value)
        expected_outcome = "1d20+3d6+5"
        self.assertEqual(outcome, expected_outcome, "Input should be the same as the output.")

    # TESTS FOR sort_dice(dice_pairs)

    def test_sort_dice_unsorted(self):
        test_input = [(1, 20), (1, 8), (1, 12), (1, 20)]
        outcome = diceroll.sort_dice(test_input)
        expected_outcome = [(2, 20), (1, 12), (1, 8)]
        self.assertEqual(expected_outcome, outcome, "{} should sort to {}".format(test_input, expected_outcome))

    def test_sort_dice_sorted(self):
        test_input = [(1, 8), (2, 6), (1, 4)]
        outcome = diceroll.sort_dice(test_input)
        # expected_outcome = [(2, 20), (1, 12), (1, 8)]
        self.assertEqual(test_input, outcome, "Sorted list should still be sorted")

    def test_sort_dice_empty(self):
        test_input = []
        outcome = diceroll.sort_dice(test_input)
        # expected_outcome = []
        self.assertEqual(test_input, outcome, "Empty set is still empty.")

    # TESTS for prune_dice(dice_pairs)

    def test_prune_dice_below_cap(self):
        test_input = [(1, 20), (1, 6)]
        outcome = diceroll.prune_dice(test_input)
        self.assertEqual(test_input, outcome, "List should not be pruned.")

    def test_prune_dice_above_cap_single(self):
        above_cap_input = settings.DHARDCAP+5
        test_input = [(above_cap_input, 20)]
        outcome_one = diceroll.prune_dice(test_input)
        expected_outcome_one = [(settings.DHARDCAP, 20)]
        self.assertEqual(expected_outcome_one, outcome_one, "List should be pruned.")

    def test_prune_dice_above_cap_multiple(self):
        below_cap_input = settings.DHARDCAP-5
        test_input = [(1, 20), (below_cap_input, 12), (1, 10), (5, 8), (3, 2), (5, 4)]
        expected_output = [(1, 20), (below_cap_input, 12), (1, 10)]
        output = diceroll.prune_dice(test_input)
        self.assertEqual(expected_output, output, "List should be pruned.")

    def test_prune_dice_above_cap_lone_integer(self):
        above_cap_input = settings.DHARDCAP+5
        test_input = [(above_cap_input, 20), (1, 6), (6, 1)]
        possibly_pruned_list = diceroll.prune_dice(test_input)
        expected_list = [(settings.DHARDCAP, 20), (6, 1)]
        self.assertEqual(expected_list, possibly_pruned_list, "List should be pruned.")

    def test_prune_dice_value_only(self):
        test_input = [(5, 1)]
        outcome_one = diceroll.prune_dice(test_input)
        expected_outcome_one = []
        self.assertEqual(expected_outcome_one, outcome_one, "List should be pruned to empty.")

    def test_prune_dice_empty(self):
        test_input = []
        outcome_one = diceroll.prune_dice(test_input)
        self.assertEqual(test_input, outcome_one, "Empty set is still empty.")


if __name__ == '__main__':
    unittest.main()
