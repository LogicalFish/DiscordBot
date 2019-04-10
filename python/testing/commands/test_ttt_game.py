import unittest

from modules.games.tictactoe.game_state import Game
import settings


class TestTicTacToeGame(unittest.TestCase):

    def test_initialization(self):
        players = ["Player 1", "Player 2"]
        game = Game(players)
        for player in players:
            self.assertIn(player, game.players.values())
        self.assertEqual(len(game.players), 2)

    def test_initialization_wrong(self):
        players = []
        with self.assertRaises(ValueError):
            Game(players)

    def test_other_player(self):
        player_one_name = "Player 1"
        player_two_name = "Player 2"
        players = [player_one_name, player_two_name]
        game = Game(players)
        self.assertEqual(settings.TTT_PIECES[0], game.turn, "Piece 1 always goes first.")
        self.assertEqual(settings.TTT_PIECES[1], game.get_other_player(), "Piece 2 should have the next turn.")

    def test_move(self):
        players = ["Player 1", "Player 2"]
        game = Game(players)
        move_validity = game.make_move("B2")
        self.assertTrue(move_validity, "Move should be valid")
        self.assertEqual(settings.TTT_PIECES[0], game.game_board.board[1][1], "Piece should be placed on the board.")
        self.assertEqual(settings.TTT_PIECES[1], game.turn, "Piece 2 should have this turn.")
        self.assertEqual(settings.TTT_PIECES[0], game.get_other_player(), "Piece 1 should have the next turn.")

    def test_wrong_move(self):
        players = ["Player 1", "Player 2"]
        game = Game(players)
        move_validity = game.make_move("B4")
        self.assertFalse(move_validity, "Move should be invalid.")
        self.assertEqual(settings.TTT_PIECES[0], game.turn, "Nothing should have changed. Player's 1 turn.")
        self.assertEqual(settings.TTT_PIECES[1], game.get_other_player(), "Piece 2 should have the next turn.")

    def test_cpu_move_easy_one(self):
        players = ["Player 1", "Player 2"]
        game = Game(players)
        cpu_move = game.get_cpu_move(1)
        move_validity = game.make_move(cpu_move)
        self.assertTrue(move_validity, "Move should be valid")
        expected_move = "A1"
        self.assertEqual(expected_move, cpu_move, "Easy mode should start top left.")

    def test_cpu_move_easy_two(self):
        players = ["Player 1", "Player 2"]
        game = Game(players)
        cpu_move = game.get_cpu_move(2)
        move_validity = game.make_move(cpu_move)
        self.assertTrue(move_validity, "Move should be valid.")

    def test_cpu_move_normal_three_first_move(self):
        players = ["Player 1", "Player 2"]
        game = Game(players)
        cpu_move = game.get_cpu_move(3)
        move_validity = game.make_move(cpu_move)
        self.assertTrue(move_validity, "Move should be valid.")

    def test_cpu_move_normal_three_block_move(self):
        players = ["Player 1", "Player 2"]
        game = Game(players)
        setup_moves = ["B1", "A1", "C2", "A2"]
        for move in setup_moves:
            self.assertTrue(game.make_move(move), "Setup should complete.")
        cpu_move = game.get_cpu_move(3)
        move_validity = game.make_move(cpu_move)
        self.assertTrue(move_validity, "Move should be valid.")
        expected_move = "A3"
        self.assertEqual(expected_move, cpu_move, "AI should block the opponent's next move.")

    def test_cpu_move_normal_three_win_move(self):
        players = ["Player 1", "Player 2"]
        game = Game(players)
        setup_moves = ["B2", "C2", "B1", "A2"]
        for move in setup_moves:
            self.assertTrue(game.make_move(move), "Setup should complete.")
        cpu_move = game.get_cpu_move(3)
        move_validity = game.make_move(cpu_move)
        self.assertTrue(move_validity, "Move should be valid.")
        expected_move = "B3"
        self.assertEqual(expected_move, cpu_move, "AI should make the winning move.")

    def test_cpu_move_hard_four_first_move(self):
        players = ["Player 1", "Player 2"]
        game = Game(players)
        cpu_move = game.get_cpu_move(4)
        move_validity = game.make_move(cpu_move)
        self.assertTrue(move_validity, "Move should be valid.")
        expected_move = "B2"
        self.assertEqual(expected_move, cpu_move, "Always go for middle first.")

    def test_cpu_move_hard_five(self):
        players = ["Player 1", "Player 2"]
        game = Game(players)
        cpu_move = game.get_cpu_move(5)
        move_validity = game.make_move(cpu_move)
        self.assertTrue(move_validity, "Move should be valid.")


if __name__ == '__main__':
    unittest.main()
