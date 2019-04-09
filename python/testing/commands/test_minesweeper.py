import unittest

from commands.modules.minesweeper import minesweeper
import settings


class TestMinesweeper(unittest.TestCase):

    def test_generate_random_spots(self):
        dimensions = (4, 6)
        amount_of_spots = 5
        spots = minesweeper.generate_random_spots(dimensions, amount_of_spots)
        self.assertIsNotNone(spots, "Output should not be None.")
        self.assertEqual(amount_of_spots, len(spots), "Should have given length")
        # Test Uniqueness:
        while spots:
            spot = spots.pop(0)
            self.assertNotIn(spot, spots, "Should all be unique.")

    def test_generate_random_spots_maximum(self):
        dimensions = (10, 8)
        amount_of_spots = 79
        spots = minesweeper.generate_random_spots(dimensions, amount_of_spots)
        self.assertIsNotNone(spots, "Output should not be None.")
        self.assertEqual(amount_of_spots, len(spots), "Should have given length")
        # Test Uniqueness:
        while spots:
            spot = spots.pop(0)
            self.assertNotIn(spot, spots, "Should all be unique.")

    def test_generate_random_spots_too_many(self):
        dimensions = (4, 6)
        amount_of_spots = 30
        with self.assertRaises(ValueError):
            minesweeper.generate_random_spots(dimensions, amount_of_spots)


if __name__ == '__main__':
    unittest.main()
