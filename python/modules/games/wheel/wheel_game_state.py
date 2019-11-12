import random

from modules.games.wheel.wheel_board import FortunateBoard


class WheelGame:
    BANKRUPT_SIGN = -10
    LOSETURN_SIGN = -5
    FREESPIN_SIGN = 0
    WILDCARD_SIGN = 50

    WHEEL = [BANKRUPT_SIGN, 90, 50, 65, 50,
             80, LOSETURN_SIGN, 70, FREESPIN_SIGN, 65,
             BANKRUPT_SIGN, 60, 50, 55, 60,
             100, 70, 50, 65, 60,
             70, 60, WILDCARD_SIGN, 250]

    FREESPIN_VALUE = 50
    VOWEL_VALUE = 25

    def __init__(self, player_set):
        self.board = FortunateBoard()
        self.players = player_set
        self.score = {}
        for player in self.players:
            self.score[player] = 0
        self.turn = 0
        self.spin_value = 0
        self.freespin = False

    def __str__(self):
        """
        :return: A string representing the current board state.
        """
        result = str(self.board)
        return result

    def get_scores_with_nicknames(self, system):
        result = "``\tCategory: {}\t".format(self.board.category)
        for player in self.players:
            result += "{}: {}\t".format(system.nickname_manager.get_name(player), "{} sp".format(self.score[player]))
        result += "``"
        return result

    def remove_player(self, player):
        self.players.remove(player)
        self.turn = self.turn % len(self.players)

    def next_turn(self):
        self.turn = (self.turn + 1) % len(self.players)

    def get_current_player(self):
        return self.players[self.turn]

    def contains_player(self, player):
        return player in self.players

    def spin_wheel(self):
        if self.spin_value > 0:
            return self.spin_value, self.get_monetary_value(self.spin_value)
        spin = self.random_spin()
        if spin > 0:
            self.spin_value = spin
            return spin, self.get_monetary_value(spin)
        if spin == self.BANKRUPT_SIGN:
            self.score[self.get_current_player()] = 0
            self.next_turn()
            return spin, "BANKRUPT"
        if spin == self.LOSETURN_SIGN:
            self.next_turn()
            return spin, "LOSE A TURN"
        if spin == self.FREESPIN_SIGN:
            self.freespin = True
            return spin, "FREE SPIN"
        return spin, "ERROR"

    def random_spin(self):
        return random.choice(self.WHEEL)

    def guess_consonant(self, guess):
        if self.freespin:
            return self.guess_free_consonant(guess)
        if self.spin_value > 0:
            guess_count = self.board.guess_consonant(guess)
            self.score[self.get_current_player()] += guess_count * self.spin_value
            self.spin_value = 0
            if guess_count == 0:
                self.next_turn()
            return guess_count
        return -1

    def guess_free_consonant(self, guess):
        guess_count = self.board.guess_consonant(guess)
        self.score[self.get_current_player()] += guess_count * self.FREESPIN_VALUE
        self.freespin = False
        return guess_count

    def buy_vowel(self, guess):
        if self.freespin:
            return self.buy_free_vowel(guess)
        if self.score[self.get_current_player()] >= self.VOWEL_VALUE:
            self.score[self.get_current_player()] -= self.VOWEL_VALUE
            guess_count = self.board.buy_vowel(guess)
            if guess_count == 0:
                self.next_turn()
            return guess_count
        return -1

    def buy_free_vowel(self, guess):
        guess_count = self.board.buy_vowel(guess)
        self.freespin = False
        return guess_count

    def solve_word(self, guess):
        solved = self.board.solve_word(guess)
        if not solved and not self.freespin:
            self.next_turn()
        self.freespin = False
        return solved

    @staticmethod
    def get_monetary_value(number):
        if number % 10 == 0:
            return "{} goudstukken".format(int(number / 10))
        else:
            return "{} zilverstukken".format(number)
