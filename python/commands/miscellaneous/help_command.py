import config
from commands.command_superclass import Command
from commands.command_error import CommandError


class HelpCommand(Command):

    def __init__(self, command_runner):
        call = ["help", "commands", "hulp", "halp"]
        parameters = "*(optional)* Name of a command."
        description = "This command will display a description and necessary parameters of a command. " \
                      "Without parameters, it will display a list of possible commands."
        super().__init__(call, parameters, description)
        self.command_runner = command_runner

    def execute(self, param, message, system):
        if len(param):
            try:
                return {"response": str(self.command_runner.get_command(param))}
            except ValueError:
                raise CommandError("command_not_found", param)
        else:
            return {"response": "**List of Commands:** {}"
                                "*Type ``{}{} <command>`` for more information.*".format(self.get_list_of_commands(),
                                                                                         config.SIGN,
                                                                                         self.call[0])}

    def get_list_of_commands(self):
        result = ""
        for i, command in enumerate(self.command_runner.commands):
            result += "\t{}{}".format(config.SIGN, command.call[0])
            if i % 3 == 2:
                result += "\n"
            else:
                result += " " * (15 - len(command.call[0]))
        result = "```{}```".format(result)
        return result
