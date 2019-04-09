import settings
from responder import parser
from commands.modules.help_command import HelpCommand
from commands.modules.dice.diceroll_command import RollCommand
from commands.modules.dice.godroll_command import GodRollCommand
from commands.modules.dice.cheat_dice_command import CheatRollCommand
from commands.modules.poll_command import PollCommand
from commands.modules.miscellaneous_commands import EchoCommand
from commands.modules.nicknames.callme_command import CallmeCommand
from commands.modules.responder_commands import StatusCommand, BanCommand, UnBanCommand,\
    ChatToggleCommand, IntervalCommand, LeaveCommand
from commands.modules.tictactoe.ttt_commands import ChallengeCommand, PlayGameCommand, AbandonGameCommand
from commands.modules.minesweeper.minesweeper_command import MineSweeperCommand
from commands.modules.calendar.calendar_commands import EventCommand, ListEventCommand, CreateEventCommand,\
    EditEventCommand, DeleteEventCommand

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
    :return: a action dictionary containing five possible actions:
        action["response"] : String: The string reply to the message.
        action["react"] : List (String): The emojis the bot needs to react with.
        action["c_react"] : List (String): The custom emojis the bot needs to react with.
        action["leave"] : Identity: The identity the bot should change to.
        action["board"] : String: Contains a Tic-Tac-Toe board, to be displayed if a game is played.
    """
    user_call, user_param = split_message(message)
    print("Attempting to execute the {} command from {}".format(user_call, message.author.name))
    try:
        command = get_command(user_call)
    except ValueError:
        return {"response": parser.direct_call(system.id_manager.current_id, "error")}
    return command.execute(user_param, message, system)


def get_command(call):
    for c in commands_list:
        if c.in_call(call):
            return c
    raise ValueError


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
