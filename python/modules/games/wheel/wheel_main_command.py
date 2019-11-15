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
        call = ["wheel", "w"]
        parameters = "The action you wish to take in the game of wheel. (Try /w help for a list of those actions)"
        description = "The game of Wheel of Fortune! " \
                      "The rules are simple: A word is displayed, but all the letters are hidden. " \
                      "The goal is to eventually guess the word.\n" \
                      "Players take turns to try to uncover the word. " \
                      "Each turn a player can choose to buy, spin, or solve.\n" \
                      "If you choose to spin, you spin the wheel and guess a consonant. " \
                      "For each of that consonant on the board, you earn the money you've spun!\n" \
                      "If you choose to buy, you can buy a vowel with the money you've earned that round, " \
                      "and it will be uncovered.\nFinally, you can try and solve the word and win the round! " \
                      "\nKeep in mind, if you buy, spin, guess or solve poorly, your turn ends..."

        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        return self.WheelRunner.run_command(param, message, system)