import settings
from commands import error_handler
from commands.command_error import CommandError
from bot_identity import parser
from bot_identity.response_commands import StatusCommand, BanCommand, UnBanCommand, ChatToggleCommand, LeaveCommand, \
    IntervalCommand
from commands.miscellaneous.help_command import HelpCommand
from commands.miscellaneous.miscellaneous_commands import EchoCommand
from commands.miscellaneous.poll_command import PollCommand
from modules.calendar.calendar_commands import EventCommand, ListEventCommand, CreateEventCommand, EditEventCommand, \
    DeleteEventCommand
from modules.dice.cheat_dice_command import CheatRollCommand
from modules.dice.diceroll_command import RollCommand
from modules.dice.godroll_command import GodRollCommand
from modules.games.minesweeper.minesweeper_command import MineSweeperCommand
from modules.games.tictactoe.ttt_commands import ChallengeCommand, PlayGameCommand, AbandonGameCommand
from modules.nicknames.nickname_command import CallmeCommand

# Complete list of commands that people can access through the bots.
commands_list = [CallmeCommand(), EchoCommand(), HelpCommand(), PollCommand(),
                 RollCommand(), GodRollCommand(), CheatRollCommand(),
                 StatusCommand(), BanCommand(), UnBanCommand(), ChatToggleCommand(), IntervalCommand(), LeaveCommand(),
                 ChallengeCommand(), PlayGameCommand(), AbandonGameCommand(), MineSweeperCommand(),
                 EventCommand(), ListEventCommand(), CreateEventCommand(), EditEventCommand(), DeleteEventCommand()]


def run_command(message, system):
    """
    Method to run a specified command.
    :param message: The message object containing the command.
    :param system: The system meta-object, containing information about the current state of the bot.
    :return: a action dictionary containing six possible actions:
        action["response"] : String: The string reply to the message.
        action["event_embed"] : Embed: A specific type of message, allowing for greater customization.
        action["react"] : List (String): The emojis the bot needs to react with.
        action["c_react"] : List (String): The custom emojis the bot needs to react with.
        action["leave"] : Identity: The identity the bot should change to.
        action["board"] : String: Contains a Tic-Tac-Toe board, to be displayed if a game is played.
    """
    user_call, user_param = split_message(message)
    print("Attempting to execute the {} command from {}".format(user_call, message.author.name))
    try:
        command = get_command(user_call)
        return command.execute(user_param, message, system)
    except CommandError as error:
        response = "{} {}".format(parser.direct_call(system.id_manager.current_id, "error"),
                                  error_handler.ERROR_DICT[error.type].format(error.key))
        return {"response": response}


def get_command(call):
    """
    Method to get a specific command based on a call. Raises an error if no command is found.
    :param call: The command string given by the client.
    :return: The command class the call belongs to.
    """
    for c in commands_list:
        if c.in_call(call):
            return c
    raise CommandError("command_not_found", call)


def split_message(message):
    """
    Splits a message's contents in two halves.
    :param message: A message.
    :return: command : A string containing the first word of the message. (The 'command')
            user_param : A string containing the rest of the message. (The 'parameters')
    """
    # Split the message contents in two halves.
    # One containing the command (first word in the string), the other the command parameters.
    splittext = message.clean_content.split(' ', 1)
    command = splittext[0][len(settings.SIGN):]
    user_param = ""
    if len(splittext) > 1:
        user_param = splittext[1]
    return command, user_param
