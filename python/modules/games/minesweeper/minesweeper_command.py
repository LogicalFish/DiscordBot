import re

from commands.command_superclass import Command
from . import minesweeper
from . import config_minesweeper as config

from commands.command_error import CommandError


class MineSweeperCommand(Command):
    """
    Command for generating a minesweeper board, based either on input or a default size.
    """

    def __init__(self):
        call = ["minesweeper", "mine"]
        parameters = "*(optional)*  A set of dimensions, as well as the bomb count. *(Example: (10, 10), 15)*."
        description = "This command will give a random minesweeper board."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        match = re.search("\\((\\d+)[,x.\\-](\\d+)\\),?(\\d+)?", param.replace(" ", ""))
        if match and int(match[1])*int(match[2]) < config.SWEEPER_MAX_SIZE:
            dimensions = (int(match[1]), int(match[2]))
            if match[3]:
                bomb_count = int(match[3])
            else:
                dividing_factor = 8 - system.id_manager.get_current_ai()
                bomb_count = int(dimensions[0]*dimensions[1]/dividing_factor)
        else:
            dimensions = config.SWEEPER_AI_TABLE[system.id_manager.get_current_ai()]
            bomb_count = config.SWEEPER_AI_BOMBS[system.id_manager.get_current_ai()]
        try:
            minefield = minesweeper.create_minefield(dimensions, bomb_count)
            minefield_string = minesweeper.minefield_to_string(minefield)
            return {"response": "**MIJNENVEGER**\n{}".format(minefield_string)}
        except ValueError as error:
            raise CommandError(str(error), param)
