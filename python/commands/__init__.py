from .run_command import CommandRunner

from bot_identity.response_commands import StatusCommand, BanCommand, UnBanCommand, \
    ChatToggleCommand, DismissCommand, IntervalCommand

from config import configuration

# Complete list of commands that people can access through the bots.
commands_list = [StatusCommand(), BanCommand(), UnBanCommand(),
                 ChatToggleCommand(), IntervalCommand(), DismissCommand()]


if configuration['commands']['poll']:
    from .miscellaneous.poll_command import PollCommand
    commands_list.append(PollCommand())
if configuration['commands']['nicknames']:
    from modules.nicknames.nickname_command import CallmeCommand
    commands_list.append(CallmeCommand())
if configuration['commands']['echo']:
    from .miscellaneous.echo_command import EchoCommand
    commands_list.append(EchoCommand())

if configuration['commands']['dice']:
    from modules.dice.diceroll_commands import RollCommand, CheatRollCommand, GodRollCommand
    commands_list.append(RollCommand())
    if configuration['commands']['god_dice']:
        commands_list.append(GodRollCommand())
    if configuration['commands']['cheat_dice']:
        commands_list.append(CheatRollCommand())

if configuration['commands']['calendar']:
    from modules.calendar.calendar_commands import EventCommand, ListEventCommand, CreateEventCommand, \
        EditEventCommand, DeleteEventCommand, UnShadowCommand

    commands_list += [EventCommand(), ListEventCommand(), CreateEventCommand(),
                      EditEventCommand(), DeleteEventCommand(), UnShadowCommand()]

if configuration['commands']['remindme']:
    from modules.reminders.reminder_command import RemindCommand
    commands_list.append(RemindCommand())

if configuration['commands']['character_list']:
    from modules.characterlist.list_commands import ListAllCommand, WhoIsCommand, AddYearCommand, GetYearCommand

    commands_list += [ListAllCommand(), WhoIsCommand(), GetYearCommand(), AddYearCommand()]

if configuration['commands']['tic-tac-toe']:
    from modules.games.tictactoe.ttt_commands import ChallengeCommand, PlayGameCommand, AbandonGameCommand
    commands_list += [ChallengeCommand(), PlayGameCommand(), AbandonGameCommand()]
if configuration['commands']['minesweeper']:
    from modules.games.minesweeper.minesweeper_command import MineSweeperCommand
    commands_list.append(MineSweeperCommand())
if configuration['commands']['wheel']:
    from modules.games.wheel.wheel_main_command import MainWheelCommand
    commands_list.append(MainWheelCommand())

MainCommand = CommandRunner(commands_list)
