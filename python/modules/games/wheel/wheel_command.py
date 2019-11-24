from bot_identity import parser
from commands.command_error import CommandError
from commands.command_superclass import Command
from config import configuration


class JoinWheelCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """

    def __init__(self):
        call = ["join", "me", "play"]
        parameters = "*(optional)* The new size of the waiting lobby."
        description = "Adds you to a lobby of players seeking to play Fortunate Wheel. " \
                      "The size of the lobby can be changed at will, and a game will start when the lobby is full." \
                      "If the size becomes too small, everyone is kicked out of the lobby."

        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        changed = False
        new_game = None
        if param:
            try:
                if int(param) > 1:
                    new_game = system.wheel_manager.change_player_count(int(param))
                    changed = True
            except ValueError:
                pass
        player = message.author
        in_game = system.wheel_manager.player_in_game(player)
        if not in_game:
            new_game = system.wheel_manager.add_to_queue(player)
        if new_game:
            contestants = self.get_nicknames_list(new_game.players, system)
            first_turn = system.nickname_manager.get_name(new_game.get_current_player())
            return {"response": parser.direct_call(system.id_manager.current_id, "wheelstart").format(contestants,
                                                                                                      first_turn),
                    "board": str(new_game),
                    "scores": new_game.get_scores_with_nicknames(system)}
        if in_game and not changed:
            return {"response": parser.direct_call(system.id_manager.current_id, "twogames")}
        wait = system.wheel_manager.get_queue_length()
        contestants = self.get_nicknames_list(system.wheel_manager.queue, system)
        return {"response": parser.direct_call(system.id_manager.current_id, "waiting").format(contestants, wait)}

    @staticmethod
    def get_nicknames_list(players, system):
        nicknames = [system.nickname_manager.get_name(p) for p in players]
        if len(nicknames) > 1:
            contestants = " & ".join([", ".join(nicknames[:-1]), nicknames[-1]])
        elif len(nicknames) == 1:
            contestants = nicknames[0]
        else:
            contestants = "ERROR"
        return contestants


class SpinWheelCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """

    def __init__(self):
        call = ["spin", "draai", "roll"]
        parameters = "None."
        description = "Attempt to spin the wheel in a game to earn money! Watch out for Lose A Turn or Bankrupt!"
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


class GuessConsonantCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """

    def __init__(self):
        call = ["guess", "consonant", "raad"]
        parameters = "The consonant you wish to guess."
        description = "Guess a consonant after you've spun the wheel! " \
                      "Keep in mind that if you guess wrong, you lose your turn."
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


class BuyVowelCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """

    def __init__(self):
        call = ["buy", "vowel", "koop", "klinker"]
        parameters = "The vowel you wish to buy."
        description = "Buy a vowel for 25 silver pieces! " \
                      "Keep in mind that if the vowel is not on the board, you lose your turn!"
        # TODO: Fetch 25 from config.
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


class SolveCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """

    def __init__(self):
        call = ["solve", "oplossen"]
        parameters = "The solution of the puzzle."
        description = "Try and solve the puzzle! " \
                      "If you get it right, all the money you won will be added to your score. " \
                      "If you get it wrong, you lose your turn!"
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
            player_name = system.nickname_manager.get_name(wheelgame.get_current_player())
            return {"response": parser.direct_call(system.id_manager.current_id, "wrongsolve").format(player_name)}


class WheelStatusCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """

    def __init__(self):
        call = ["status", "board", "wheel"]
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
        call = ["quit", "abandon"]
        parameters = "None."
        description = "Leave the game you are currently a part of."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        player = message.author
        game_left = system.wheel_manager.leave_game(player)

        if game_left:
            return {"response": parser.direct_call(system.id_manager.current_id, "wheelgone").format(
                system.nickname_manager.get_name(player))}
        return {"response": parser.direct_call(system.id_manager.current_id, "nogame")}


class WheelScoreCommand(Command):

    def __init__(self):
        call = ["score"]
        parameters = "None."
        description = "Check your total winnings from the Game of Wheel."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        player = message.author

        if message.guild:
            scores = system.wheel_manager.get_highscore_table()
            score_line = []
            for score in scores:
                player = system.get_user_by_id(score.user_id, guild=message.guild)
                if player:
                    player_name = system.nickname_manager.get_name(player)
                    player_score = system.wheel_manager.get_monetary_value(score.score)
                    spacing = " " * (configuration['nicknames']['max_length'] - len(player_name))
                    line = "{i}: {name}{s}-\t{score}".format(i=len(score_line)+1, s=spacing, name=player_name, score=player_score)
                    score_line.append(line)
            if len(score_line):
                return {"response": "```{}```".format("\n".join(score_line))}
            raise CommandError("database_error", None)
        else:
            player_name = system.nickname_manager.get_name(player)
            score = system.wheel_manager.get_highscore(player)
            spacing = " " * (configuration['nicknames']['max_length'] - len(player_name))
            return {"response": "```{i}: {name}{s}-\t{score}```".format(i=1, s=spacing, name=player_name, score=score)}

    def in_call(self, command):
        if "score" in command:
            return True
        return False
