from commands.command_superclass import Command
from modules.games.tictactoe import game_flow as game


class ChallengeCommand(Command):

    """
    Command class for challenging someone to a game of Tic-Tac-Toe.
    """

    def __init__(self):
        super().__init__('tic_tac_toe_challenge')

    def execute(self, param, message, system):
        if len(message.mentions) > 0:
            challenged = message.mentions[0]
        else:
            challenged = system.bot
        print("Starting a new game between {} and {}".format(message.author.name, challenged.name))
        response, board = game.tictactoenewgame(message.author, challenged, system)
        return {"response": response, "board": board}


class PlayGameCommand(Command):

    """
    Command class for playing Tic-Tac-Toe.
    """

    def __init__(self):
        super().__init__('tic_tac_toe_move')

    def in_call(self, command):
        if command in self.call:
            return True
        if len(command) == 0:
            return False
        for char in command:
            if char != "t":
                return False
        return True

    def execute(self, param, message, system):
        print("{} is attempting move _{}_".format(message.author.name, param))
        response, board = game.tictactoemove(param, message.author, system)
        return {"response": response, "board": board}


class AbandonGameCommand(Command):

    """
    Command class for abandoning a game of Tic-Tac-Toe.
    """

    def __init__(self):
        super().__init__('tic_tac_toe_abandon')

    def execute(self, param, message, system):
        print("{} has abandoned their game".format(message.author.name))
        return {"response": game.tictactoeend(message.author, system)}
