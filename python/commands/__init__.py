from .run_command import CommandRunner

from bot_identity.response_commands import StatusCommand, BanCommand, UnBanCommand, ChatToggleCommand, DismissCommand, \
    IntervalCommand
from .miscellaneous.echo_command import EchoCommand
from .miscellaneous.poll_command import PollCommand
from modules.dice.diceroll_commands import RollCommand, CheatRollCommand, GodRollCommand
from modules.games.tictactoe.ttt_commands import ChallengeCommand, PlayGameCommand, AbandonGameCommand
from modules.games.minesweeper.minesweeper_command import MineSweeperCommand
from modules.games.wheel.wheel_main_command import MainWheelCommand
from modules.nicknames.nickname_command import CallmeCommand
from modules.reminders.reminder_command import RemindCommand
from modules.characterlist.list_commands import ListAllCommand, WhoIsCommand, AddYearCommand, GetYearCommand

from config import configuration

# Complete list of commands that people can access through the bots.
commands_list = [EchoCommand(), PollCommand(),
                 CallmeCommand(),
                 RollCommand(), GodRollCommand(), CheatRollCommand(),
                 StatusCommand(), BanCommand(), UnBanCommand(),
                 ChatToggleCommand(), IntervalCommand(), DismissCommand(),
                 ChallengeCommand(), PlayGameCommand(), AbandonGameCommand(),
                 MineSweeperCommand(),
                 RemindCommand(),
                 ListAllCommand(), WhoIsCommand(), GetYearCommand(), AddYearCommand(),
                 MainWheelCommand()]

if configuration['calendar']['active']:
    from modules.calendar.calendar_commands import EventCommand, ListEventCommand, CreateEventCommand, \
        EditEventCommand, DeleteEventCommand, UnShadowCommand

    commands_list += [EventCommand(), ListEventCommand(), CreateEventCommand(),
                      EditEventCommand(), DeleteEventCommand(), UnShadowCommand()]


MainCommand = CommandRunner(commands_list)
