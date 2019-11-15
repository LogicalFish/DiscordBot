import math
from sqlalchemy import func

from database.models.high_score_model import Score
from modules.games.wheel.wheel_game_state import WheelGame


class WheelManager:
    DEFAULT_PLAYER_COUNT = 3

    def __init__(self, database_manager):
        self.player_count = self.DEFAULT_PLAYER_COUNT
        self.queue = []
        self.games = []
        self.high_scores = {}
        self.database = database_manager

    def change_player_count(self, new_count):
        if new_count < len(self.queue):
            self.queue = []
        self.player_count = new_count
        return self.new_game()

    def add_to_queue(self, player):
        self.queue.append(player)
        return self.new_game()

    def new_game(self):
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
        # return False #TODO

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
        if self.database is not None:
            score = self.database.fetch_one(Score, player.id)
            if score:
                return self.get_monetary_value(score.score)
        return self.get_monetary_value(0)

    def get_highscore_table(self):
        if self.database is not None:
            session = self.database.Session()
            scores = session.query(Score).order_by(Score.score.desc()).all()
            session.expunge_all()
            session.close()
            return scores
        return []

    def add_score(self, player, score):
        if self.database is not None:
            session = self.database.Session()
            current_score = session.query(Score).filter(Score.user_id == player.id).first()
            if current_score:
                current_score.score += score
            else:
                session.add(Score(player.id, score))
            session.commit()
            session.close()

    @staticmethod
    def get_monetary_value(number):
        result = []
        if number > 100:
            count = math.floor(number / 100)
            result.append("{c} platinumstuk{plural}".format(c=count, plural="ken" if count > 1 else ""))
            number = number % 100
        if number > 10:
            count = math.floor(number / 10)
            result.append("{c} goudstuk{plural}".format(c=count, plural="ken" if count > 1 else ""))
            number = number % 10
        if number > 0:
            count = math.floor(number)
            result.append("{c} zilverstuk{plural}".format(c=count, plural="ken" if count > 1 else ""))
        if len(result) == 0:
            return "0 koperstukken"
        return ", ".join(result)
