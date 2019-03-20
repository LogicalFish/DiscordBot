import settings


class Command:

    def __init__(self, call, parameters="None.", description=""):
        self.call = call
        self.parameters = parameters
        self.description = description

    def __str__(self):
        return "**Command(s):** *{}*.\n" \
               "**Description:** {}\n" \
               "**Parameter(s):** {}".format(self.get_call_string(),
                                             self.description,
                                             self.parameters)

    def get_call_string(self):
        result = ""
        for item in self.call:
            if result:
                result += ", "
            result += settings.SIGN + item
        return result

    def in_call(self, command):
        return command in self.call

    def execute(self, param, message, system):
        raise NotImplementedError
