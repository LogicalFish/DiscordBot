from bot_identity import parser
from commands.command_error import CommandError
from commands.command_superclass import Command
from modules.nicknames import nickname_config


class JoinWheelCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """

    def __init__(self):
        call = ["wheelme", "joinwheel", "wheelplay"]
        parameters = "*(optional)* The size of the waiting lobby. Will kick everyone out if lobby becomes too small."
        description = "Adds you to a lobby of players seeking to play Fortunate Wheel. " \
                      "A game will start when the lobby is full."

        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        changed = False
        if param:
            try:
                if int(param) > 1:
                    system.wheel_manager.change_player_count(int(param))
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
        elif not changed:
            return {"response": parser.direct_call(system.id_manager.current_id, "twogames")}
        wait = system.wheel_manager.get_queue_length()
        contestants = self.get_nicknames_list(system.wheel_manager.queue, system)
        return {"response": parser.direct_call(system.id_manager.current_id, "waiting").format(contestants, wait)}

    def in_call(self, command):
        if command in self.call:
            return True
        if "wheel" in command and ("join" in command or "play" in command):
            return True
        return False

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
        game_left = system.wheel_manager.leave_game(player)

        if game_left:
            return {"response": parser.direct_call(system.id_manager.current_id, "wheelgone").format(
                system.nickname_manager.get_name(player))}
        return {"response": parser.direct_call(system.id_manager.current_id, "nogame")}


class WheelScoreCommand(Command):

    def __init__(self):
        call = ["wheelscore", "highscore"]
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
                    spacing = " " * (nickname_config.MAX_NICK_NAME - len(player_name))
                    line = "{i}: {name}{s}-\t{score}".format(i=len(score_line)+1, s=spacing, name=player_name, score=player_score)
                    score_line.append(line)
            if len(score_line):
                return {"response": "```{}```".format("\n".join(score_line))}
            raise CommandError("database_error", None)
        else:
            player_name = system.nickname_manager.get_name(player)
            score = system.wheel_manager.get_highscore(player)
            spacing = " " * (nickname_config.MAX_NICK_NAME - len(player_name))
            return {"response": "```{i}: {name}{s}-\t{score}```".format(i=1, s=spacing, name=player_name, score=score)}

    def in_call(self, command):
        if "score" in command:
            return True
        return False
