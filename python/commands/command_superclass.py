import config


class Command:
    """
    Command superclass, defining how a command should be structured.
    """

    def __init__(self, call, parameters="None.", description=""):
        """
        Three values should be initialized during initialization.
        :param call: A list detailing which phrases should trigger this command.
        :param parameters: A written explanation of the parameters that the command expects.
        :param description: A written explanation of what the command does.
        """
        self.call = call
        self.parameters = parameters
        self.description = description

    def __str__(self):
        """
        As a string, the command should give an explanation of how to call it, what parameters it takes,
        and a description of what it does.
        """
        return "**Command(s):** *{}*.\n" \
               "**Description:** {}\n" \
               "**Parameter(s):** {}".format(self.get_call_string(),
                                             self.description,
                                             self.parameters)

    def get_call_string(self):
        """
        Helper method to convert the call list to a string.
        :return: A string containing the list of possible calls the command responds to.
        """
        result = ""
        for item in self.call:
            if result:
                result += ", "
            result += config.SIGN + item
        return result

    def in_call(self, command):
        """
        Method for determining if a specific string would trigger this command. Can be overwritten.
        :param command:
        :return:
        """
        return command in self.call

    def execute(self, param, message, system):
        """
        Method to be implemented by the class. Executes the actual command when it's calledw.
        :param param: The parameters given by the user.
        :param message: The message meta-data, including who sent the command.
        :param system: The system object, for accessing different managers.
        :return:
        """
        raise NotImplementedError
