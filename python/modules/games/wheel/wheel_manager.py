import math

from modules.games.wheel.wheel_game_state import WheelGame


class WheelManager:
    DEFAULT_PLAYER_COUNT = 3

    def __init__(self):
        self.player_count = self.DEFAULT_PLAYER_COUNT
        self.queue = []
        self.games = []
        self.high_scores = {}

    def change_player_count(self, new_count):
        if new_count < len(self.queue):
            self.queue = []
        self.player_count = new_count

    def add_to_queue(self, player):
        self.queue.append(player)
        if len(self.queue) == self.player_count:
            new_game = WheelGame(self.queue)
            self.games.append(new_game)
            self.queue = []
            return new_game
        return None

    def get_queue_length(self):
        return self.player_count - len(self.queue)

    def get_game(self, player):
        for wheelgame in self.games:
            if wheelgame.contains_player(player):
                return wheelgame
        return None

    def player_in_game(self, player):
        for game in self.games:
            if game.contains_player(player):
                return True
        return player in self.queue
        # return False

    def leave_game(self, player):
        if player in self.queue:
            self.queue.remove(player)
            return True
        game = self.get_game(player)
        if game is not None:
            game.remove_player(player)
            if len(game.players) == 0:
                self.games.remove(game)
            return True
        return False

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
