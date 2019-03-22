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
            return {"response": "**List of Commands:** {}"
                                "*Type *``{}{} <command>``* for more information.*".format(self.get_list_of_commands(),
                                                                                           settings.SIGN,
                                                                                           self.call[0])}

    @staticmethod
    def get_list_of_commands():
        result = ""
        for i, command in enumerate(run_command.commands_list):
            result += "\t{}{}".format(settings.SIGN, command.call[0])
            if i % 3 == 2:
                result += "\n"
            else:
                for i in range(15-len(command.call[0])):
                    result += " "
        result = "```{}```".format(result)
        return result
