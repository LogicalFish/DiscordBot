import random
import settings

MINE = "💣"
NUMBERS = ["⬜", "1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣"]


def create_minefield(dimensions, bomb_amount):
    minefield = []
    for i in range(dimensions[1]):
        row = []
        for j in range(dimensions[0]):
            row.append(settings.FREE_SPACE)
        minefield.append(row)

    bombs = generate_random_spots(dimensions, bomb_amount)
    for bomb in bombs:
        minefield[bomb[1]][bomb[0]] = MINE

    minefield = allocate_numbers(minefield)

    return minefield


def minefield_to_string(minefield):
    minefield_string = ""
    for row in minefield:
        for square in row:
            minefield_string += "||{}||".format(square)
        minefield_string += "\n"
    return minefield_string


def generate_random_spots(dimensions, spots):
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
        raise ValueError("Can't have more bombs than squares.")


def upgrade_number(number):
    number_index = NUMBERS.index(number)
    return NUMBERS[number_index+1]


def allocate_numbers(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is MINE:
                for n in range(i-1, i+2):
                    for m in range(j-1, j+2):
                        if 0 <= n < len(board) and 0 <= m < len(board[n]) and board[n][m] is not MINE:
                            board[n][m] = upgrade_number(board[n][m])
    return board
