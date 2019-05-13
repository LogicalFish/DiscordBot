import random

from . import config_minesweeper as config

def create_minefield(dimensions, bomb_amount):
    """
    Method for generating a 'minefield' based on the popular game "minesweeper".
    :param dimensions: A double tuple containing the dimensions of the minefield. (Width x Height)
    :param bomb_amount: The amount of mines on the field.
    :return: A double array representing a game board. Each entry contains either a mine or a number.
    """
    minefield = []
    if dimensions[0] < 2 or dimensions[1] < 2:
        raise ValueError("board_too_small")
    for i in range(dimensions[1]):
        row = []
        for j in range(dimensions[0]):
            row.append(config.SWEEPER_NUMBERS[0])
        minefield.append(row)

    bombs = generate_random_spots(dimensions, bomb_amount)
    for bomb in bombs:
        minefield[bomb[1]][bomb[0]] = config.SWEEPER_MINE

    minefield = allocate_numbers(minefield)

    return minefield


def minefield_to_string(minefield):
    """
    Generates a string-version of a minefield.
    :param minefield: The minefield to convert to string.
    :return: A string containing a minefield.
    """
    minefield_string = ""
    for row in minefield:
        for square in row:
            minefield_string += "{0}{1}{0}".format(config.SWEEPER_DELIMITER, square)
        minefield_string += "\n"
    return minefield_string


def generate_random_spots(dimensions, spots):
    """
    Generates a list of random spots on a board. Useful for generating mines.
    :param dimensions: The dimensions of the board.
    :param spots: The amount of spots you need.
    :return: A list of unique spots.
    """
    permutations = dimensions[0] * dimensions[1]
    if spots < permutations:
        result_matrix = []
        while len(result_matrix) < spots:
            random_square = (random.randint(0, dimensions[0]-1),
                             random.randint(0, dimensions[1]-1))
            if random_square not in result_matrix:
                result_matrix.append(random_square)
        return result_matrix
    else:
        raise ValueError("too_many_bombs")


def upgrade_number(number):
    """
    Takes a "number" from the field, and returns the next sequential number.
    :param number: The number token.
    :return: A number token representing the next number.
    """
    number_index = config.SWEEPER_NUMBERS.index(number)
    return config.SWEEPER_NUMBERS[number_index + 1]


def allocate_numbers(board):
    """
    Takes a minefield with mines, and generates the proper numbers for each
    :param board: The minefield.
    :return: The board.
    """
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is config.SWEEPER_MINE:
                for n in range(i-1, i+2):
                    for m in range(j-1, j+2):
                        if 0 <= n < len(board) and 0 <= m < len(board[n]) and board[n][m] is not config.SWEEPER_MINE:
                            board[n][m] = upgrade_number(board[n][m])
    return board
