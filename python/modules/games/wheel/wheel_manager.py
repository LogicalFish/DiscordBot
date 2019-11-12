import math


class WheelManager:

    def __init__(self):
        self.games = []
        self.high_scores = {}

    def get_game(self, player):
        for wheelgame in self.games:
            if wheelgame.contains_player(player):
                return wheelgame
        return None

    def get_highscore(self, player):
        if player in self.high_scores:
            return get_monetary_value(self.high_scores[player])
        return get_monetary_value(0)

    def get_highest_score(self):
        high_score = 0
        high_player = None
        for player in self.high_scores:
            if self.high_scores[player] > high_score:
                high_score = self.high_scores[player]
                high_player = player
        return high_player, get_monetary_value(high_score)

    def add_score(self, player, score):
        if player in self.high_scores:
            self.high_scores[player] += score
        else:
            self.high_scores[player] = score


def get_monetary_value(number):
    result = []
    if number > 100:
        result.append("{} platinumstukken".format(math.floor(number / 100)))
        number = number % 100
    if number > 10:
        result.append("{} goudstukken".format(math.floor(number / 10)))
        number = number % 10
    if number > 0:
        result.append("{} zilverstukken".format(math.floor(number)))
    if len(result) == 0:
        return "0 koperstukken"
    return ", ".join(result)
