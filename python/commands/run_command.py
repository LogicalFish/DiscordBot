import config
from commands.command_error import CommandError
from .miscellaneous.help_command import HelpCommand


class CommandRunner:

    errors = config.localization['errors']

    def __init__(self, commands_list):
        self.commands = commands_list
        self.help = HelpCommand(self)
        self.commands.append(self.help)

    def run_command(self, params, message, system):
        """
        Method to run a specified command.
        :param params: The parameters given to the command
        :param message: The message object containing the command.
        :param system: The system meta-object, containing information about the current state of the bot.
        :return: a action dictionary containing six possible actions:
            action["response"] : String: The string reply to the message.
            action["event_embed"] : Embed: A specific type of message, allowing for greater customization.
            action["react"] : List (String): The emojis the bot needs to react with.
            action["c_react"] : List (String): The custom emojis the bot needs to react with.
            action["leave"] : Identity: The identity the bot should change to.
            action["board"] : String: Contains a Tic-Tac-Toe board, to be displayed if a game is played.
        """
        user_call, user_param = self.split_message(params)
        user_call = user_call.lower()
        print("Attempting to execute the {} command from {}".format(user_call, message.author.name))
        try:
            command = self.get_command(user_call)
            return command.execute(user_param, message, system)
        except CommandError as error:
            response = "{} {}".format(system.id_manager.id_statement("general", "error"),
                                      self.errors[error.type].format(error.key))
            return {"response": response}

    def get_command(self, call):
        """
        Method to get a specific command based on a call. Raises an error if no command is found.
        :param call: The command string given by the client.
        :return: The command class the call belongs to.
        """
        for c in self.commands:
            if c.in_call(call):
                return c
        raise CommandError("command_not_found", call)

    @staticmethod
    def split_message(full_command):
        """
        Splits a message's contents in two halves.
        :param full_command: The full command
        :return: command : A string containing the first word of the message. (The 'command')
                user_param : A string containing the rest of the message. (The 'parameters')
        """
        # Split the message contents in two halves.
        # One containing the command (first word in the string), the other the command parameters.
        splittext = full_command.split(' ', 1)
        user_param = splittext[1] if len(splittext) > 1 else ""
        return splittext[0], user_param
