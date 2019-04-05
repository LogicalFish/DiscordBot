import copy
import random
import settings as s
from .board import Board


# GAME class. Keeps track of a tic-tac-toe game, including players, turns, and NPC moves
class Game:
    """
    Attributes:
        turn: The Token of the player whose turn it is.
    """
    turn = s.TTT_PIECES[0]

    def __init__(self, input_players):
        """
        Initializes the game
        :param input_players: A list containing two players.
        """
        self.game_board = Board()
        self.players = {}
        if len(input_players) == 2:
            random.shuffle(input_players)
            for i in range(2):
                self.players[s.TTT_PIECES[i]] = input_players[i]
        else:
            raise ValueError

    def __str__(self):
        """
        :return: A string representing the current board state.
        """
        result = str(self.game_board)
        result = "THE BOARD:" + result
        return result

    def get_other_player(self):
        """
        :return: Returns the token representing the player other than the one whose turn it is.
        """
        for p in s.TTT_PIECES:
            if p != self.turn:
                return p

    def get_status(self):
        """
        Return the status of the game.
        :return: Tuple containing the following two values:
            Boolean: True if the game has been won/ended. False if no one has won.
            String: The token of the winning player. "T" if the game has tied.
            If no one has won, returns the token of the current player.
        """
        if self.game_board.get_win():
            return True, self.game_board.get_win()
        else:
            return self.game_board.get_win(), self.turn,

    def make_move(self, move):
        """
        Makes a move on the board, and if the move is valid, gives the turn to the next player
        :param move: The move to be made.
        :return: Boolean representing validity of move.
        """
        valid = self.game_board.make_move(move, self.turn)
        if valid:
            self.turn = self.get_other_player()
            return valid

    def get_cpu_move(self, difficulty):
        """
        Artificial Intelligence method. Will pick a move depending on the supplied difficulty.
        :param difficulty: A positive non-zero integer with a maximum of 5.
        Each integer represents a different tactic:
        > 1 = In Order
        > 2 = Random
        > 3 = Random, but will always make winning moves, or block opponent's winning moves.
        > 4 = Will always go for middle square first, otherwise same as #3
        > 5 = Unbeatable. Will never lose, always tie if they can't win.
        Integers higher than 5 will be treated as 5. Integers of 0 and lower will be treated as 2.
        :return: A valid move.
        """
        moves = self.game_board.get_set(s.FREE_SPACE)
        #DIFFICULTY 3 (Normal Mode) Strategy
        if difficulty > 2:
            order = [self.turn, self.get_other_player()]
            for o in order:
                for move in moves:
                    board_copy = copy.copy(self.game_board)
                    board_copy.make_move(move, o)
                    if board_copy.get_win() == o:
                        return move
            #DIFFICULTY 4 (Normal + / Hard mode) Strategy
            if difficulty > 3:
                if "B2" in moves:
                    return "B2"
                #DIFFICULTY 5 (Expert) Strategy
                if difficulty > 4:
                    other_moves = self.game_board.get_set(self.get_other_player())
                    diagonals = ["A1","A3","C1","C3"]
                    if len(other_moves) == 2:
                        if set(other_moves).issubset(set(diagonals)):
                            return "C2"
                        for move in moves:
                            if move in diagonals and self.game_board.get_opposite(move) in moves:
                                if self.get_other_player() in self.game_board.get_adjacent(move):
                                    return move
                                else:
                                    potential_move = move
                        return potential_move
                    elif len(other_moves) == 1:
                        for move in moves:
                            if move in diagonals and self.game_board.get_opposite(move) in moves\
                                    and self.get_other_player() not in self.game_board.get_adjacent(move):
                                return move
        # DIFFICULTY 1 (Simple) Strategy
        elif difficulty == 1:
            return moves[0]
        # DIFFICULTY 2 Code (+fall-through for higher difficulties)
        return random.choice(moves)
