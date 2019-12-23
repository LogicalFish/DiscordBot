from commands.command_superclass import Command
from commands import CommandRunner

from modules.games.wheel.wheel_command import JoinWheelCommand, SpinWheelCommand, GuessConsonantCommand, \
    BuyVowelCommand, SolveCommand, WheelStatusCommand, WheelQuitCommand, WheelScoreCommand


class MainWheelCommand(Command):
    """
    Command class for challenging someone to a game of Wheel
    """
    wheel_commands_list = [JoinWheelCommand(), SpinWheelCommand(), GuessConsonantCommand(), BuyVowelCommand(),
                           SolveCommand(), WheelStatusCommand(), WheelQuitCommand(), WheelScoreCommand()]

    WheelRunner = CommandRunner(wheel_commands_list)

    def __init__(self):
        super().__init__('wheel_main')

    def execute(self, param, message, system):
        return self.WheelRunner.run_command(param, message, system)
