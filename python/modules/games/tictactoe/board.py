import copy

from . import ttt_config as config


class Board:
    """
    BOARD class. Keeps track of a Tic-Tac-Toe board, and handles any changes to it.
    Attributes:
        DIMENSION: The Dimension of the Game-Board. Should be kept at 3 unless you know what you're doing.
        ROWS: String/List containing the three labels for each row.
        COLUMNS: String/List containing the three labels for each column.
        board: two-dimensional list, containing a 3x3 playing board.
    """
    DIMENSION = 3
    ROWS = "123"
    COLUMNS = "ABC"
    TIE_TOKEN = "T"

    def __init__(self):
        """
        Initializes the board attribute: a 3x3 board filled with 'empty' squares.
        """
        self.board = []
        for i in range(self.DIMENSION):
            row = []
            for j in range(self.DIMENSION):
                row.append(config.FREE_SPACE)
            self.board.append(row)

    def __str__(self):
        """
        :return: A string representing the current board state.
        """
        result = "\n"
        result += config.CANTON
        result += "".join(config.DISPLAY_COLUMNS)
        for i in range(self.DIMENSION):
            result += "\n"
            result += config.DISPLAY_ROWS[i]
            for j in range(self.DIMENSION):
                result += self.board[i][j]
        return result

    def __copy__(self):
        """
        :return: A copy of the board, which does not change the current board.
        """
        board_copy = Board()
        board_copy.board = copy.deepcopy(self.board)
        return board_copy

    def make_move(self, move, player):
        """
        A method that, if supplied with a valid move
        :param move: A String. If it represents an empty square on the board, it is a valid move.
        :param player: The piece that is to be placed on the board.
        :return: True if the move is valid. False if the move could not be made.
        """
        if not isinstance(move, str):
            return False
        if len(move) >= 2 and move[0] in self.COLUMNS and move[1] in self.ROWS:
            v = ord(move[0].lower()) - 97 #Converts Alphabetical order to number. (A=0)
            h = int(move[1])-1

            if self.board[h][v] == config.FREE_SPACE:
                self.board[h][v] = player
                return True
        return False

    def get_win(self):
        """
        A method that checks if anyone has won a game on the current board.
        :return: False if no one has won. String T if the game has tied. Otherwise, the token that has won.
        """
        for i in range(self.DIMENSION):
            if self.board[i][i] != config.FREE_SPACE:
                if self.board[i][0] == self.board[i][1] == self.board[i][2]:
                    return self.board[i][0]
                elif self.board[0][i] == self.board[1][i] == self.board[2][i]:
                    return self.board[0][i]
        if self.board[1][1] != config.FREE_SPACE:
            if self.board[0][0] == self.board[1][1] == self.board[2][2]:
                return self.board[1][1]
            elif self.board[2][0] == self.board[1][1] == self.board[0][2]:
                return self.board[1][1]
        if len(self.get_set(config.FREE_SPACE)) == 0:
            return self.TIE_TOKEN
        return False

    def get_set(self, token):
        """
        Returns a list of squares occupied by the chosen token.
        :param token: The token (can also be free space) to be checked for.
        :return: A list of squares, each occupied by the chosen token.
        """
        squares = []
        for i in range(self.DIMENSION):
            for j in range(self.DIMENSION):
                if self.board[j][i] == token:
                    squares.append("{}{}".format(self.COLUMNS[i], self.ROWS[j]))
        return squares

    def get_adjacent(self, tile):
        """
        A helper method for AI. Checks each tile adjacent to the chosen tile and returns their contents.
        :param tile: A square on the board.
        :return: A list of the tokens adjacent to the chosen tile
        """
        result = []
        if tile[0] in self.COLUMNS and tile[1] in self.ROWS:
            v = ord(tile[0].lower()) - 97
            h = int(tile[1]) - 1
        for x in [-1,1]:
            if 0 <= v-x < self.DIMENSION:
                result.append(self.board[h][v-x])
            if 0 <= h-x < self.DIMENSION:
                result.append(self.board[h-x][v])
        return result

    def get_opposite(self, tile):
        """
        Helper method for AI. Returns the tile that is diametrically opposed to the supplied tile.
        B2 (center tile) is its own opposite.
        :param tile: A square on the board.
        :return: The coordinates of the opposing tile.
        """
        result = ""
        result += self.COLUMNS[(self.COLUMNS.find(tile[0]) + 1) * -1]
        result += self.ROWS[(self.ROWS.find(tile[1]) + 1) * -1]
        return result
