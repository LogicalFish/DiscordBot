import random

import config
from modules.games.wheel.wheel_board import WheelBoard
wheel_config = config.configuration['wheel']


class WheelGame:

    def __init__(self, player_set):
        self.board = WheelBoard()
        self.players = player_set
        self.score = {}
        for player in self.players:
            self.score[player] = 0
        self.turn = random.randrange(0, len(self.players))
        self.wheel = wheel_config['wheel_layout']
        self.spin_value = 0
        self.freespin = False

    def __str__(self):
        """
        :return: A string representing the current board state.
        """
        result = str(self.board)
        return result

    def get_scores_with_nicknames(self, system):
        result = "``\t{0}: {1}\t".format(config.localization['wheel']['category'], self.board.category)
        for player in self.players:
            result += "{player}: {n} {sp}\t".format(player=system.nickname_manager.get_name(player),
                                                    n=self.score[player],
                                                    sp=config.localization['wheel']['sp_a'])
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
        if isinstance(spin, int):
            self.spin_value = spin
            return spin, self.get_monetary_value(spin)
        if spin == "BANKRUPT":
            self.score[self.get_current_player()] = 0
            self.next_turn()
            return spin, config.localization['wheel']['bankrupt']
        if spin == "LOSETURN":
            self.next_turn()
            return spin, config.localization['wheel']['lose_turn']
        if spin == "FREESPIN":
            self.freespin = True
            return spin, config.localization['wheel']['free_spin']
        return spin, "ERROR"

    def random_spin(self):
        return random.choice(self.wheel)

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
        self.score[self.get_current_player()] += guess_count * wheel_config['freespin_value']
        self.freespin = False
        return guess_count

    def buy_vowel(self, guess):
        if self.freespin:
            return self.buy_free_vowel(guess)
        if self.score[self.get_current_player()] >= wheel_config['vowel_cost']:
            self.score[self.get_current_player()] -= wheel_config['vowel_cost']
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
            return "{n} {gp}{plural}".format(n=int(number / 10), gp=config.localization['wheel']['gp'],
                                             plural=config.localization['wheel']['plural'])
        else:
            return "{n} {sp}{plural}".format(n=number, sp=config.localization['wheel']['sp'],
                                             plural=config.localization['wheel']['plural'])
