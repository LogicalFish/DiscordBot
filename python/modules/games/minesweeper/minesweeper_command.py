import re

from commands.command_superclass import Command
from modules.games.minesweeper import minesweeper

from commands.command_error import CommandError


class MineSweeperCommand(Command):

    MAX_LENGTH = 198
    AI_table = {1: (6, 4), 2: (8, 6), 3: (12, 8), 4: (14, 10), 5: (18, 11)}
    bomb_table = {1: 1, 2: 5, 3: 14, 4: 25, 5: 40}

    def __init__(self):
        call = ["minesweeper", "mine"]
        parameters = "A set of dimensions, as well as the bomb count. (Example: (10, 10), 15"
        description = "This command will give a random minesweeper board."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        match = re.search("\\((\\d+)[,x.\\-](\\d+)\\),?(\\d+)?", param.replace(" ", ""))
        if match and int(match[1])*int(match[2]) < self.MAX_LENGTH:
            dimensions = (int(match[1]), int(match[2]))
            if match[3]:
                bomb_count = int(match[3])
            else:
                dividing_factor = 8 - system.id_manager.get_current_ai()
                bomb_count = int(dimensions[0]*dimensions[1]/dividing_factor)
        else:
            dimensions = self.AI_table[system.id_manager.get_current_ai()]
            bomb_count = self.bomb_table[system.id_manager.get_current_ai()]
        try:
            minefield = minesweeper.create_minefield(dimensions, bomb_count)
            return {"response": minesweeper.minefield_to_string(minefield)}
        except ValueError as error:
            raise CommandError(str(error), param)
