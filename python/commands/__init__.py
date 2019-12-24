from .run_command import CommandRunner

from bot_identity.response_commands import StatusCommand, BanCommand, UnBanCommand, ChatToggleCommand, DismissCommand, \
    IntervalCommand
from .miscellaneous.echo_command import EchoCommand
from .miscellaneous.poll_command import PollCommand
from modules.nicknames.nickname_command import CallmeCommand
from modules.reminders.reminder_command import RemindCommand

from config import configuration

# Complete list of commands that people can access through the bots.
commands_list = [EchoCommand(), PollCommand(),
                 CallmeCommand(),
                 StatusCommand(), BanCommand(), UnBanCommand(),
                 ChatToggleCommand(), IntervalCommand(), DismissCommand(),
                 RemindCommand()]

if configuration['dice']['active']:
    from modules.dice.diceroll_commands import RollCommand, CheatRollCommand, GodRollCommand
    commands_list.append(RollCommand())
    if configuration['dice']['god_module']:
        commands_list.append(GodRollCommand())
    if configuration['dice']['cheat_module']:
        commands_list.append(CheatRollCommand())

if configuration['calendar']['active']:
    from modules.calendar.calendar_commands import EventCommand, ListEventCommand, CreateEventCommand, \
        EditEventCommand, DeleteEventCommand, UnShadowCommand

    commands_list += [EventCommand(), ListEventCommand(), CreateEventCommand(),
                      EditEventCommand(), DeleteEventCommand(), UnShadowCommand()]

if configuration['character_list']['active']:
    from modules.characterlist.list_commands import ListAllCommand, WhoIsCommand, AddYearCommand, GetYearCommand

    commands_list += [ListAllCommand(), WhoIsCommand(), GetYearCommand(), AddYearCommand()]

if configuration['tic-tac-toe']['active']:
    from modules.games.tictactoe.ttt_commands import ChallengeCommand, PlayGameCommand, AbandonGameCommand
    commands_list += [ChallengeCommand(), PlayGameCommand(), AbandonGameCommand()]
if configuration['minesweeper']['active']:
    from modules.games.minesweeper.minesweeper_command import MineSweeperCommand
    commands_list.append(MineSweeperCommand())
if configuration['wheel']['active']:
    from modules.games.wheel.wheel_main_command import MainWheelCommand
    commands_list.append(MainWheelCommand())

MainCommand = CommandRunner(commands_list)
