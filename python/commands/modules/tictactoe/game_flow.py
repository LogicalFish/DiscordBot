from .game_state import Game
from responder import parser


def tictactoenewgame(author, opponent, system):
    """
    Start a new game of Tic-Tac-Toe
    :param author: The Creator of the game.
    :param opponent: The opponent, which may be a human or the bot.
    :param system: The system meta-object, containing information about the current bot-state.
    :return: response (String): A response based on the current identity of the bot,
        signifying either a new game, or the game status if a game already existed.
        str(game) (string): A representation of the game board.
    """
    if author in system.ttt_games or opponent in system.ttt_games:
        if author in system.ttt_games:
            game = system.ttt_games[author]
        elif opponent in system.ttt_games:
            game = system.ttt_games[opponent]
        response = parser.direct_call(system.current_id, "gamestate").format(
            system.get_name(game.players[game.turn]),
            system.get_name(game.players[game.get_other_player()])
        )
    else:
        game = Game([author, opponent])
        system.ttt_games[author] = game
        if opponent != system.bot:
            system.ttt_games[opponent] = game
        current_player = game.players[game.turn]
        if current_player == system.bot:
            response = parser.direct_call(system.current_id, "open").format("Ik ben")
            tictactoemove("cpu", author, system)
        else:
            response = parser.direct_call(system.current_id, "open").format("{} is".format(system.get_name(current_player)))
    return response, str(game)


#Ends a Tic-Tac-Toe game and removes all references to it.
def tictactoeend(author, system):
    """
    Ends a game of tic-tac-toe, and removes all references to it.
    :param author: One of the (human) participants of the game.
    :param system: The system meta-object, containing information about the current bot-state.
    :return: A response based on the current identity of the bot,
        signifying either that the game has been abandoned, or an error if no game was found.

    """
    if author in system.ttt_games:
        game = system.ttt_games[author]
        for key in game.players:
            system.ttt_games.pop(game.players[key], None)
            if game.players[key] != author:
                other_player = game.players[key]
        return parser.direct_call(system.current_id, "abandon").format(system.get_name(author),
                                                                       get_addressable(system, other_player))
    else: return parser.direct_call(system.current_id, "error")


def tictactoemove(text, author, system):
    """
    Makes a move in a game of tic-tac-toe, and immediately makes a CPU move if it's their turn.
    If no game of tic-tac-toe is found, create one, and make the move if it is valid.
    :param text: The parameters supplied by the user.
    :param author: The user making the move OR in case of a CPU move: The other user associated with the game.
    :param system: The system meta-object, containing information about the current bot-state.
    :return: esponse (String): A response based on the current identity of the bot,
        signifying either a new game if none existed, the gamestate if no parameters are found,
        the move made by the bot, or the victory/tie of either party
        str(game) (string): A representation of the game board.

    """
    response = ""
    if author in system.ttt_games:
        game = system.ttt_games[author]
    else:
        #Starting a new game if none exists:
        response = "{}\n".format(tictactoenewgame(author, system.bot, system)[0])
        game = system.ttt_games[author]

    #Replying with a status:
    if text == "" and response == "":
        opponent = game.players[game.get_other_player()]
        player_name = get_addressable(system, game.players[game.turn])
        opponent_name = get_addressable(system, opponent)
        response = parser.direct_call(system.current_id, "gamestate").format(player_name, opponent_name)
        return response, game
    #Making a move:
    move = ""
    if game.players[game.turn] == system.bot:
        move = game.get_cpu_move(system.get_current_ai())
        response += parser.direct_call(system.current_id, "ownmove").format(game.turn, move) +"\n"
    elif game.players[game.turn] == author:
        move = text[:2].upper()
        if game.players[game.get_other_player()] != system.bot:
            response = parser.direct_call(system.current_id, "gamestate").format(
                system.get_name(game.players[game.get_other_player()]),
                system.get_name(game.players[game.turn])
            )
    valid = game.make_move(move)

    if not valid and text != "":
        response = parser.direct_call(system.current_id, "invalid")
        return response, str(game)
    #Handling a winstate
    win_state, w_p = game.get_status()
    if win_state:
        tictactoeend(author, system)
        if w_p == "T":
            response += parser.direct_call(system.current_id, "tie")
        else:
            if game.players[w_p] == system.bot:
                response += parser.direct_call(system.current_id, "win")
            elif system.bot in game.players.values():
                response += parser.direct_call(system.current_id, "loss")
            else:
                response += parser.direct_call(system.current_id, "genericwin").format(
                    system.get_name(game.players[w_p]),
                    system.get_name(game.players[game.turn]))
        return response, str(game)
    #If there's a CPU, have him make a move.
    if game.players[game.turn] == system.bot:
        response += tictactoemove("cpu", author, system)[0]
    return response, str(game)


def get_addressable(system, player):
    if player == system.bot:
        return "mij"
    else:
        return system.get_name(player)
