import re
import config

from commands.command_superclass import Command
from commands.command_error import CommandError

from . import minesweeper

mine_config = config.configuration['minesweeper']


class MineSweeperCommand(Command):
    """
    Command for generating a minesweeper board, based either on input or a default size.
    """

    def __init__(self):
        super().__init__('minesweeper')

    def execute(self, param, message, system):
        match = re.search("\\((\\d+)[,x.\\-](\\d+)\\),?(\\d+)?", param.replace(" ", ""))
        if match and int(match[1])*int(match[2]) < mine_config['max_size']:
            dimensions = (int(match[1]), int(match[2]))
            if match[3]:
                bomb_count = int(match[3])
            else:
                dividing_factor = 8 - system.id_manager.get_current_ai()
                bomb_count = int(dimensions[0]*dimensions[1]/dividing_factor)
        else:
            dimensions = mine_config['AI_table'][system.id_manager.get_current_ai()]
            bomb_count = mine_config['AI_bombs'][system.id_manager.get_current_ai()]
        try:
            minefield = minesweeper.create_minefield(dimensions, bomb_count)
            minefield_string = minesweeper.minefield_to_string(minefield)
            return {"response": config.localization[self.name]['title'].format(minefield_string)}
        except ValueError as error:
            raise CommandError(str(error), param)
