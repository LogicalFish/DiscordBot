from .run_command import CommandRunner

from bot_identity.response_commands import StatusCommand, BanCommand, UnBanCommand, ChatToggleCommand, LeaveCommand, \
    IntervalCommand
from .miscellaneous.miscellaneous_commands import EchoCommand
from .miscellaneous.poll_command import PollCommand
from modules.calendar.calendar_commands import EventCommand, ListEventCommand, CreateEventCommand, EditEventCommand, \
    DeleteEventCommand, UnShadowCommand
from modules.dice.cheat_dice_command import CheatRollCommand
from modules.dice.diceroll_command import RollCommand
from modules.dice.godroll_command import GodRollCommand
from modules.games.minesweeper.minesweeper_command import MineSweeperCommand
from modules.games.tictactoe.ttt_commands import ChallengeCommand, PlayGameCommand, AbandonGameCommand
from modules.games.wheel.wheel_command import JoinWheelCommand, SpinWheelCommand, GuessConsonantCommand, \
    BuyVowelCommand, SolveCommand, WheelStatusCommand, WheelQuitCommand
from modules.nicknames.nickname_command import CallmeCommand

from modules.characterlist.list_commands import ListAllCommand, WhoIsCommand, AddYearCommand, GetYearCommand

# Complete list of commands that people can access through the bots.
commands_list = [CallmeCommand(), EchoCommand(), PollCommand(),
                 RollCommand(), GodRollCommand(), CheatRollCommand(),
                 StatusCommand(), BanCommand(), UnBanCommand(), ChatToggleCommand(), IntervalCommand(), LeaveCommand(),
                 ChallengeCommand(), PlayGameCommand(), AbandonGameCommand(), MineSweeperCommand(),
                 EventCommand(), ListEventCommand(), CreateEventCommand(), EditEventCommand(), DeleteEventCommand(),
                 UnShadowCommand(),
                 ListAllCommand(), WhoIsCommand(), GetYearCommand(), AddYearCommand(),
                 JoinWheelCommand(), SpinWheelCommand(), GuessConsonantCommand(), BuyVowelCommand(), SolveCommand(),
                 WheelStatusCommand(), WheelQuitCommand()]

MainCommand = CommandRunner(commands_list)
