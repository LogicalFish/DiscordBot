import copy
import unittest

from commands.modules.tictactoe.board import Board
import settings


class TestTicTacToeBoard(unittest.TestCase):

    def test_initialization(self):
        board = Board()
        expected_board = [[settings.FREE_SPACE, settings.FREE_SPACE, settings.FREE_SPACE],
                          [settings.FREE_SPACE, settings.FREE_SPACE, settings.FREE_SPACE],
                          [settings.FREE_SPACE, settings.FREE_SPACE, settings.FREE_SPACE]]
        self.assertEqual(expected_board, board.board, "Board should contain only empty spaces.")

    def test_copy(self):
        board_one = Board()
        board_copy = copy.copy(board_one)
        self.assertIsNot(board_one, board_copy, "Copy should be deepcopy, not the same instance.")
        self.assertIsNot(board_one.board, board_copy.board, "Copy should be deepcopy, not the same instance.")
        self.assertEqual(board_one.board, board_copy.board, "Copies of the board should contain same values.")

    def test_make_move_valid(self):
        board = Board()
        move = "B3"
        player = "X"
        expected_board = [[settings.FREE_SPACE, settings.FREE_SPACE, settings.FREE_SPACE],
                          [settings.FREE_SPACE, settings.FREE_SPACE, settings.FREE_SPACE],
                          [settings.FREE_SPACE, "X", settings.FREE_SPACE]]
        return_boolean = board.make_move(move, player)
        self.assertTrue(return_boolean, "True means move was valid.")
        self.assertEqual(expected_board, board.board, "Board should have new value.")

    def test_make_all_valid_moves(self):
        board = Board()
        player = "X"
        valid_moves = ["A1", "B1", "C1", "A2", "B2", "C2", "A3", "B3", "C3"]
        for move in valid_moves:
            return_boolean = board.make_move(move, player)
            self.assertTrue(return_boolean, "All moves should have been valid.")

    def test_make_move_invalid(self):
        board = Board()
        old_board = copy.copy(board.board)
        player = "X"
        invalid_moves = ["A0", "Z3", "AA", "22", 34, ("AB", "23"), ["A1", "B2"]]
        for move in invalid_moves:
            return_boolean = board.make_move(move, player)
            self.assertFalse(return_boolean, "Invalid moves should result in False.")
        self.assertEqual(old_board, board.board, "Board should be same as before.")

    def test_get_win_no_win(self):
        board = Board()
        player = "X"
        moves = ["A1", "B1", "C3"]
        for move in moves:
            board.make_move(move, player)
        self.assertFalse(board.get_win(), "Game should not be won yet.")

    def test_get_win_horizontal_win(self):
        board = Board()
        player = "X"
        moves = ["A1", "A2", "A3"]
        for move in moves:
            board.make_move(move, player)
        self.assertEqual(player, board.get_win(), "Game should be won by X.")

    def test_get_win_vertical_win(self):
        board = Board()
        player = "X"
        moves = ["A1", "B1", "C1"]
        for move in moves:
            board.make_move(move, player)
        self.assertEqual(player, board.get_win(), "Game should be won by X.")

    def test_get_win_diagonal_win(self):
        board = Board()
        player = "X"
        moves = ["A3", "B2", "C1"]
        for move in moves:
            board.make_move(move, player)
        self.assertEqual(player, board.get_win(), "Game should be won by X.")

    def test_get_win_tie(self):
        board = Board()
        player_one = "X"
        player_two = "O"
        moves_one = ["B2", "A2", "B1", "A3", "C3"]
        moves_two = ["A1", "C2", "B3", "C1"]
        for move in moves_one:
            board.make_move(move, player_one)
        for move in moves_two:
            board.make_move(move, player_two)
        self.assertEqual(board.TIE_TOKEN, board.get_win(), "Game should be a tie.")

    def test_get_set(self):
        board = Board()
        player = "X"
        moves = ["B2", "A2", "B1", "A3", "C3"]
        for move in moves:
            board.make_move(move, player)
        set_of_moves = board.get_set(player)
        self.assertCountEqual(moves, set_of_moves, "Should have same contents")

    def test_get_set_empty(self):
        board = Board()
        player = "X"
        moves = []
        self.assertEqual(moves, board.get_set(player), "No moves made means no moves found")

    def test_get_adjacent_middle(self):
        board = Board()
        player_one = "X"
        player_two = "O"
        moves_one = ["B1", "B2", "B3"]
        moves_two = ["A1", "A2", "A3"]
        for move in moves_one:
            board.make_move(move, player_one)
        for move in moves_two:
            board.make_move(move, player_two)
        adjacent = board.get_adjacent("B2")
        expected_adjacent = [player_one, player_two, player_one, settings.FREE_SPACE]
        self.assertCountEqual(expected_adjacent, adjacent, "Should contain two X tokens, one O, one Free Space")

    def test_get_adjacent_corner(self):
        board = Board()
        player_one = "X"
        player_two = "O"
        moves_one = ["B1", "B2", "B3"]
        moves_two = ["A1", "A2", "A3"]
        for move in moves_one:
            board.make_move(move, player_one)
        for move in moves_two:
            board.make_move(move, player_two)
        adjacent = board.get_adjacent("A1")
        expected_adjacent = [player_one, player_two]
        self.assertCountEqual(expected_adjacent, adjacent, "Should contain one X token, one O token.")

    def test_get_opposite_corner(self):
        board = Board()
        tile = "A1"
        expected_opposite = "C3"
        opposite = board.get_opposite(tile)
        self.assertEqual(expected_opposite, opposite, "Opposite of A1 should be C3")

    def test_get_opposite_side(self):
        board = Board()
        tile = "C2"
        expected_opposite = "A2"
        opposite = board.get_opposite(tile)
        self.assertEqual(expected_opposite, opposite, "Opposite of A1 should be C3")

    def test_get_opposite_middle(self):
        board = Board()
        tile = "B2"
        expected_opposite = "B2"
        opposite = board.get_opposite(tile)
        self.assertEqual(expected_opposite, opposite, "B2 has no opposite. (Should return itself)")


if __name__ == '__main__':
    unittest.main()
