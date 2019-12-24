from commands.command_error import CommandError
from commands.command_superclass import Command
from config import configuration


class JoinWheelCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """

    def __init__(self):
        super().__init__('wheel_join')

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
            first_turn = system.name_manager.get_name(new_game.get_current_player())
            return {"response": system.id_manager.id_statement("wheel", "wheelstart").format(contestants,
                                                                                             first_turn),
                    "board": str(new_game),
                    "scores": new_game.get_scores_with_nicknames(system)}
        if in_game and not changed:
            raise CommandError("game_duplicate", param)
        wait = system.wheel_manager.get_queue_length()
        contestants = self.get_nicknames_list(system.wheel_manager.queue, system)
        return {"response": system.id_manager.id_statement("wheel", "waiting").format(contestants, wait)}

    @staticmethod
    def get_nicknames_list(players, system):
        nicknames = [system.name_manager.get_name(p) for p in players]
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
        super().__init__('wheel_spin')

    def execute(self, param, message, system):
        player = message.author
        wheelgame = system.wheel_manager.get_game(player)
        if wheelgame is None:
            raise CommandError("no_game", param)
        if wheelgame.get_current_player() is not player:
            current_player = system.name_manager.get_name(wheelgame.get_current_player())
            raise CommandError("not_turn", current_player)
        spin_value, spin_text = wheelgame.spin_wheel()
        if isinstance(spin_value, int):
            return {"response": system.id_manager.id_statement("wheel", "goodspin").format(spin_text)}
        elif spin_value == "FREESPIN":
            return {"response": system.id_manager.id_statement("wheel", "freespin")}
        else:
            opponent = system.name_manager.get_name(wheelgame.get_current_player())
            return {"response": system.id_manager.id_statement("wheel", "badspin").format(spin_text, opponent)}


class GuessConsonantCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """

    def __init__(self):
        super().__init__('wheel_guess')

    def execute(self, param, message, system):
        player = message.author
        wheelgame = system.wheel_manager.get_game(player)

        if wheelgame is None:
            raise CommandError("no_game", param)
        if wheelgame.get_current_player() is not player:
            current_player = system.name_manager.get_name(wheelgame.get_current_player())
            raise CommandError("not_turn", current_player)
        if not wheelgame.board.is_valid_character(param):
            raise CommandError("invalid_character", param)
        if wheelgame.board.is_vowel(param):
            raise CommandError("not_consonant", param)
        if wheelgame.spin_value == 0 and not wheelgame.freespin:
            raise CommandError("no_guess", param)
        count = wheelgame.guess_consonant(param)
        if count == 0:
            opponent = system.name_manager.get_name(wheelgame.get_current_player())
            return {"response": system.id_manager.id_statement("wheel", "badguess").format(param, opponent),
                    "board": str(wheelgame),
                    "scores": wheelgame.get_scores_with_nicknames(system)}
        return {"response": system.id_manager.id_statement("wheel", "goodguess").format(count, param),
                "board": str(wheelgame),
                "scores": wheelgame.get_scores_with_nicknames(system)}


class BuyVowelCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """

    def __init__(self):
        super().__init__('wheel_buy')

    def execute(self, param, message, system):
        player = message.author
        wheelgame = system.wheel_manager.get_game(player)

        if wheelgame is None:
            raise CommandError("no_game", param)
        if wheelgame.get_current_player() is not player:
            current_player = system.name_manager.get_name(wheelgame.get_current_player())
            raise CommandError("not_turn", current_player)
        if not wheelgame.board.is_valid_character(param):
            raise CommandError("invalid_character", param)
        if not wheelgame.board.is_vowel(param):
            raise CommandError("not_vowel", param)
        if wheelgame.spin_value != 0 and not wheelgame.freespin:
            raise CommandError("already_spun", param)
        if wheelgame.score[player] < configuration['wheel']['vowel_cost'] and not wheelgame.freespin:
            raise CommandError("no_cash", param)
        count = wheelgame.buy_vowel(param)
        if count == 0:
            opponent = system.name_manager.get_name(wheelgame.get_current_player())
            return {"response": system.id_manager.id_statement("wheel", "badguess").format(param, opponent),
                    "board": str(wheelgame),
                    "scores": wheelgame.get_scores_with_nicknames(system)}
        return {"response": system.id_manager.id_statement("wheel", "goodguess").format(count, param),
                "board": str(wheelgame),
                "scores": wheelgame.get_scores_with_nicknames(system)}


class SolveCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """

    def __init__(self):
        super().__init__('wheel_solve')

    def execute(self, param, message, system):
        player = message.author
        wheelgame = system.wheel_manager.get_game(player)

        if wheelgame is None:
            raise CommandError("no_game", param)
        if wheelgame.get_current_player() is not player:
            current_player = system.name_manager.get_name(wheelgame.get_current_player())
            raise CommandError("not_turn", current_player)
        if wheelgame.spin_value != 0 and not wheelgame.freespin:
            raise CommandError("already_spun", param)
        solved = wheelgame.solve_word(param)
        player_name = system.name_manager.get_name(player)
        if solved:
            score_text = wheelgame.get_monetary_value(wheelgame.score[player])
            system.wheel_manager.add_score(player, wheelgame.score[player])
            system.wheel_manager.games.remove(wheelgame)
            return {"response": system.id_manager.id_statement("wheel", "wheelwin").format(player_name,
                                                                                           score_text),
                    "board": str(wheelgame),
                    "scores": wheelgame.get_scores_with_nicknames(system)}
        else:
            player_name = system.name_manager.get_name(wheelgame.get_current_player())
            return {"response": system.id_manager.id_statement("wheel", "wrongsolve").format(player_name)}


class WheelStatusCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """

    def __init__(self):
        super().__init__('wheel_status')

    def execute(self, param, message, system):
        player = message.author
        wheelgame = system.wheel_manager.get_game(player)

        if wheelgame is None:
            raise CommandError("no_game", param)
        turn = system.name_manager.get_name(wheelgame.get_current_player())
        return {"response": system.id_manager.id_statement("wheel", "wheelturn").format(turn),
                "board": str(wheelgame),
                "scores": wheelgame.get_scores_with_nicknames(system)}


class WheelQuitCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """

    def __init__(self):
        super().__init__('wheel_quit')

    def execute(self, param, message, system):
        player = message.author
        game_left = system.wheel_manager.leave_game(player)

        if game_left:
            return {"response": system.id_manager.id_statement("wheel", "wheelgone").format(
                system.name_manager.get_name(player))}
        raise CommandError("no_game", param)


class WheelScoreCommand(Command):

    def __init__(self):
        super().__init__('wheel_score')

    def execute(self, param, message, system):
        player = message.author

        if message.guild:
            scores = system.wheel_manager.get_highscore_table()
            score_line = []
            for score in scores:
                player = system.get_user_by_id(score.user_id, guild=message.guild)
                if player:
                    player_name = system.name_manager.get_name(player)
                    player_score = system.wheel_manager.get_monetary_value(score.score)
                    spacing = " " * (configuration['nicknames']['max_length'] - len(player_name))
                    line = "{i}: {name}{s}-\t{score}".format(i=len(score_line)+1, s=spacing,
                                                             name=player_name, score=player_score)
                    score_line.append(line)
            if len(score_line):
                return {"response": "```{}```".format("\n".join(score_line))}
            raise CommandError("database_error", None)
        else:
            player_name = system.name_manager.get_name(player)
            score = system.wheel_manager.get_highscore(player)
            spacing = " " * (configuration['nicknames']['max_length'] - len(player_name))
            return {"response": "```{i}: {name}{s}-\t{score}```".format(i=1, s=spacing, name=player_name, score=score)}

    def in_call(self, command):
        if "score" in command:
            return True
        return False
