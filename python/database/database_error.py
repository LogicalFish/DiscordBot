

class DatabaseError(Exception):
    """
    Special Error Class, to be thrown when the database can't be initialized correctly.
    """

    def __init__(self, error_type):
        super().__init__(error_type)
        self.type = error_type

    def __str__(self):
        return self.type
