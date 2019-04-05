from commands.command_superclass import Command
from commands.modules.tictactoe import game_flow as game


class ChallengeCommand(Command):

    def __init__(self):
        call = ["tttchallenge", "challenge", "ttc"]
        parameters = "*(optional)* A mention of the user you wish to challenge"
        description = "Challenge another user to a Tic-Tac-Toe game. " \
                      "This fails if either user is already involved in a game."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        if len(message.mentions) > 0:
            challenged = message.mentions[0]
        else:
            challenged = system.bot
        print("Starting a new game between {} and {}".format(message.author.name, challenged.name))
        response, board = game.tictactoenewgame(message.author, challenged, system)
        return {"response": response, "board": board}


class PlayGameCommand(Command):

    def __init__(self):
        call = ["ttt", "tic-tac-toe"]
        parameters = "Coordinates of the move you wish to make on the board. *(optional)*"
        description = "Make a move in your current tic-tac-toe game, " \
                      "or show the current status if the parameter is missing. " \
                      "If you are not participating in a game, it starts a new one against the bot."
        super().__init__(call, parameters, description)

    def in_call(self, command):
        if command in self.call:
            return True
        for char in command:
            if char != "t":
                return False
        return True

    def execute(self, param, message, system):
        print("{} is attempting move _{}_".format(message.author.name, param))
        response, board = game.tictactoemove(param, message.author, system)
        return {"response": response, "board": board}


class AbandonGameCommand(Command):

    def __init__(self):
        call = ["tttabandon", "abandon", "tta"]
        parameters = "None."
        description = "Abandons all tic-tac-toe games involving you."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        print("{} has abandoned their game".format(message.author.name))
        return {"response": game.tictactoeend(message.author, system)}
