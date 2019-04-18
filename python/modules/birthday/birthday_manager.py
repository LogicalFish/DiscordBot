import datetime

NAME_TABLE = "birthdays"
PRIMARY_KEY = "user_id"
SECONDARY = "birthday"


class BirthdayManager:
    """
    Class for keeping track of user's birthdays.
    Uses a database for storing birthdays.
    """

    def __init__(self, database_manager):
        self.database = database_manager
        self.birthdays = []
        self.initialize_birthdays()

    def initialize_birthdays(self):
        """
        Initializes the data within the class, reading it from a database.
        """
        rows = self.database.get_rows(NAME_TABLE)
        for row in rows:
            self.birthdays.append((row[1], row[0]))

    def get_today_birthdays(self):
        """
        Generate a list of everyone whose birthday is today.
        :return: A list of everyone whose birthday is today. (Possibly empty)
        """
        today_birthdays = []
        for birthday in self.birthdays:
            if datetime.date.today().month == birthday[0].month and datetime.date.today().day == birthday[0].day:
                today_birthdays.append(birthday[1])
        return today_birthdays
