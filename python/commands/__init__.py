from .run_command import CommandRunner

from bot_identity.response_commands import StatusCommand, BanCommand, UnBanCommand, ChatToggleCommand, LeaveCommand, \
    IntervalCommand
from .miscellaneous.help_command import HelpCommand
from .miscellaneous.miscellaneous_commands import EchoCommand
from .miscellaneous.poll_command import PollCommand
from modules.calendar.calendar_commands import EventCommand, ListEventCommand, CreateEventCommand, EditEventCommand, \
    DeleteEventCommand, UnShadowCommand
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
                 EventCommand(), ListEventCommand(), CreateEventCommand(), EditEventCommand(), DeleteEventCommand(),
                 UnShadowCommand()]

MainCommand = CommandRunner(commands_list)
