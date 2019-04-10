
class CommandError(Exception):
    """
    Special Error Class, to be thrown when a command is not called correctly.
    """

    def __init__(self, error_type, error_key):
        super().__init__(error_type)
        self.type = error_type
        self.key = error_key

    def __str__(self):
        return "Error: {}, Parameters: {}".format(self.type, self.key)
