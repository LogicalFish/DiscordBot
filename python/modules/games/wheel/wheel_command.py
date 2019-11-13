from bot_identity import parser
from commands.command_superclass import Command
from modules.games.wheel import wheel_config
from modules.games.wheel.wheel_game_state import WheelGame


class JoinWheelCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """
    DEFAULT_PLAYER_COUNT = 3

    def __init__(self):
        self.player_count = self.DEFAULT_PLAYER_COUNT
        call = ["wheelme", "joinwheel", "wheelplay"]
        parameters = "None."
        description = "Adds you to a pool of players seeking to play Fortunate Wheel. " \
                      "A game will start when {} members have joined.".format(self.player_count)

        self.players = []
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        player = message.author
        if param == "leave" or param == "-1" and player in self.players:
            self.players.remove(player)
            return {}
        if self.player_in_game(player, system):
            return {"response": parser.direct_call(system.id_manager.current_id, "twogames")}
        if param:
            try:
                if int(param) > 1:
                    self.players = []
                    self.player_count = int(param)
            except ValueError:
                pass
        self.players.append(player)
        contestants = self.player_list(system)
        if len(self.players) == self.player_count:
            new_game = WheelGame(self.players)
            system.wheel_manager.games.append(new_game)
            first_turn = system.nickname_manager.get_name(new_game.get_current_player())
            self.players = []
            return {"response": parser.direct_call(system.id_manager.current_id, "wheelstart").format(contestants,
                                                                                                      first_turn),
                    "board": str(new_game),
                    "scores": new_game.get_scores_with_nicknames(system)}
        wait = self.player_count - len(self.players)
        return {"response": parser.direct_call(system.id_manager.current_id, "waiting").format(contestants, wait)}

    def in_call(self, command):
        if command in self.call:
            return True
        if "wheel" in command and ("join" in command or "play" in command):
            return True
        return False

    def player_in_game(self, player, system):
        for wheelgame in system.wheel_manager.games:
            if wheelgame.contains_player(player):
                return True
        return player in self.players
        # return False

    def player_list(self, system):
        result = ""
        i = len(self.players) - 1
        while i >= 0:
            result = system.nickname_manager.get_name(self.players[i]) + result
            if i == len(self.players) - 1 and i > 0:
                result = " & " + result
            elif i > 0:
                result = ", " + result
            i -= 1
        return result


class SpinWheelCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """

    def __init__(self):
        call = ["wheelspin", "spin", "spinwheel", "draai"]
        parameters = "None."
        description = "Attempt to spin the wheel in a game to earn money!"
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        player = message.author
        wheelgame = system.wheel_manager.get_game(player)
        if wheelgame is None:
            return {"response": parser.direct_call(system.id_manager.current_id,
                                                   "nogame")}
        if wheelgame.get_current_player() is not player:
            current_player = system.nickname_manager.get_name(wheelgame.get_current_player())
            return {"response": parser.direct_call(system.id_manager.current_id, "noturn").format(current_player)}
        spin_value, spin_text = wheelgame.spin_wheel()
        if spin_value > 0:
            return {"response": parser.direct_call(system.id_manager.current_id,
                                                   "goodspin").format(spin_text)}
        elif spin_value == 0:
            return {"response": parser.direct_call(system.id_manager.current_id,
                                                   "freespin")}
        else:
            opponent = system.nickname_manager.get_name(wheelgame.get_current_player())
            return {"response": parser.direct_call(system.id_manager.current_id,
                                                   "badspin").format(spin_text, opponent)}

    def in_call(self, command):
        if "spin" in command or "draai" in command:
            return True
        return False


class GuessConsonantCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """

    def __init__(self):
        call = ["wheelguess", "guess", "consonant", "raad"]
        parameters = "Guess a consonant!"
        description = "."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        player = message.author
        wheelgame = system.wheel_manager.get_game(player)

        if wheelgame is None:
            return {"response": parser.direct_call(system.id_manager.current_id, "nogame")}
        if wheelgame.get_current_player() is not player:
            current_player = system.nickname_manager.get_name(wheelgame.get_current_player())
            return {"response": parser.direct_call(system.id_manager.current_id, "noturn").format(current_player)}
        if not wheelgame.board.is_valid_character(param):
            return {"response": parser.direct_call(system.id_manager.current_id, "nocharacter").format(param)}
        if wheelgame.board.is_vowel(param):
            return {"response": parser.direct_call(system.id_manager.current_id, "noconsonant").format(param)}
        if wheelgame.spin_value == 0 and not wheelgame.freespin:
            return {"response": parser.direct_call(system.id_manager.current_id, "noguess").format(param)}
        count = wheelgame.guess_consonant(param)
        if count == 0:
            opponent = system.nickname_manager.get_name(wheelgame.get_current_player())
            return {"response": parser.direct_call(system.id_manager.current_id, "badguess").format(param, opponent),
                    "board": str(wheelgame),
                    "scores": wheelgame.get_scores_with_nicknames(system)}
        return {"response": parser.direct_call(system.id_manager.current_id, "goodguess").format(count, param),
                "board": str(wheelgame),
                "scores": wheelgame.get_scores_with_nicknames(system)}

    def in_call(self, command):
        if "guess" in command or command.startswith("raad"):
            return True
        return False


class BuyVowelCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """

    def __init__(self):
        call = ["wheelbuy", "buyvowel", "vowel", "klinker"]
        parameters = "Guess a consonant!"
        description = "."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        player = message.author
        wheelgame = system.wheel_manager.get_game(player)

        if wheelgame is None:
            return {"response": parser.direct_call(system.id_manager.current_id, "nogame")}
        if wheelgame.get_current_player() is not player:
            current_player = system.nickname_manager.get_name(wheelgame.get_current_player())
            return {"response": parser.direct_call(system.id_manager.current_id, "noturn").format(current_player)}
        if not wheelgame.board.is_valid_character(param):
            return {"response": parser.direct_call(system.id_manager.current_id, "nocharacter").format(param)}
        if not wheelgame.board.is_vowel(param):
            return {"response": parser.direct_call(system.id_manager.current_id, "novowel").format(param)}
        if wheelgame.spin_value != 0 and not wheelgame.freespin:
            return {"response": parser.direct_call(system.id_manager.current_id, "spun").format(param)}
        if wheelgame.score[player] < wheelgame.VOWEL_VALUE and not wheelgame.freespin:
            return {"response": parser.direct_call(system.id_manager.current_id, "wheelcash").format(param)}
        count = wheelgame.buy_vowel(param)
        if count == 0:
            opponent = system.nickname_manager.get_name(wheelgame.get_current_player())
            return {"response": parser.direct_call(system.id_manager.current_id, "badguess").format(param, opponent),
                    "board": str(wheelgame),
                    "scores": wheelgame.get_scores_with_nicknames(system)}
        return {"response": parser.direct_call(system.id_manager.current_id, "goodguess").format(count, param),
                "board": str(wheelgame),
                "scores": wheelgame.get_scores_with_nicknames(system)}

    def in_call(self, command):
        if "vowel" in command or "klinker" in command or "buy" in command:
            return True
        return False


class SolveCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """

    def __init__(self):
        call = ["wheelsolve", "solve"]
        parameters = "Try and solve the puzzle!"
        description = "."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        player = message.author
        wheelgame = system.wheel_manager.get_game(player)

        if wheelgame is None:
            return {"response": parser.direct_call(system.id_manager.current_id, "nogame")}
        if wheelgame.get_current_player() is not player:
            current_player = system.nickname_manager.get_name(wheelgame.get_current_player())
            return {"response": parser.direct_call(system.id_manager.current_id, "noturn").format(current_player)}
        if wheelgame.spin_value != 0 and not wheelgame.freespin:
            return {"response": parser.direct_call(system.id_manager.current_id, "spun").format(param)}
        solved = wheelgame.solve_word(param)
        player_name = system.nickname_manager.get_name(player)
        if solved:
            score_text = wheelgame.get_monetary_value(wheelgame.score[player])
            system.wheel_manager.add_score(player, wheelgame.score[player])
            system.wheel_manager.games.remove(wheelgame)
            return {"response": parser.direct_call(system.id_manager.current_id, "wheelwin").format(player_name,
                                                                                                    score_text),
                    "board": str(wheelgame),
                    "scores": wheelgame.get_scores_with_nicknames(system)}
        else:
            return {"response": parser.direct_call(system.id_manager.current_id, "wrongsolve").format(player_name)}

    def in_call(self, command):
        if "solve" in command:
            return True
        return False


class WheelStatusCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """

    def __init__(self):
        call = ["wheelstatus", "wheel", "wheelboard"]
        parameters = "None."
        description = "Shows the current game you are in."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        player = message.author
        wheelgame = system.wheel_manager.get_game(player)

        if wheelgame is None:
            return {"response": parser.direct_call(system.id_manager.current_id, "nogame")}
        turn = system.nickname_manager.get_name(wheelgame.get_current_player())
        return {"response": parser.direct_call(system.id_manager.current_id, "wheelturn").format(turn),
                "board": str(wheelgame),
                "scores": wheelgame.get_scores_with_nicknames(system)}


class WheelQuitCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """

    def __init__(self):
        call = ["wheelquit", "wheelabandon"]
        parameters = "None."
        description = "Leave the game you are currently a part of."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        player = message.author
        wheelgame = system.wheel_manager.get_game(player)

        if wheelgame is None:
            return {"response": parser.direct_call(system.id_manager.current_id, "nogame")}
        wheelgame.remove_player(player)
        if len(wheelgame.players) == 0:
            system.wheel_manager.games.remove(wheelgame)
        return {"response": parser.direct_call(system.id_manager.current_id, "wheelgone").format(
            system.nickname_manager.get_name(wheelgame.get_current_player()))}


class WheelScoreCommand(Command):

    def __init__(self):
        call = ["wheelscore", "highscore"]
        parameters = "None."
        description = "Check your total winnings from the Game of Wheel."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        player = None
        if "total" in param:
            player, score = system.wheel_manager.get_highest_score()
        if player is None:
            player = message.author
            score = system.wheel_manager.get_highscore(player)
        player_name = system.nickname_manager.get_name(player)
        return {"response": "{}: {}".format(player_name, score)}

    def in_call(self, command):
        if "score" in command:
            return True
        return False