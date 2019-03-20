import settings
from commands.command import Command
from commands import run_command


class HelpCommand(Command):

    def __init__(self):
        call = ["help", "hulp", "halp"]
        parameters = "*(optional)* Name of a command."
        description = "This command will display a description and necessary parameters of a command. " \
                      "Without parameters, it will display a list of possible commands."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        if len(param):
            try:
                return {"response": run_command.get_command(param)}
            except ValueError:
                return {"response": "[ERROR]: Command *{}{}* not found.".format(settings.SIGN, param)}
        else:
            return {"response": "**List of Commands:** {}".format(self.get_list_of_commands())}

    @staticmethod
    def get_list_of_commands():
        result = ""
        for command in run_command.commands_list:
            if result:
                result += ", "
            result += "*{}*".format(command.call[0])
        result += "."
        return result
