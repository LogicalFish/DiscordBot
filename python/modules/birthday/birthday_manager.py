import datetime

from database.models.birthday_model import Birthday


class BirthdayManager:
    """
    Class for keeping track of user's birthdays.
    Uses a database for storing birthdays.
    """

    def __init__(self, database_manager):
        self.birthdays = []
        self.database = database_manager
        if self.database is not None:
            self.initialize_birthdays()

    def initialize_birthdays(self):
        """
        Initializes the data within the class, reading it from a database.
        """
        session = self.database.Session()
        birthdays = session.query(Birthday).all()
        for birthday in birthdays:
            self.birthdays.append((birthday.birthday, birthday.user_id))
        session.commit()
        session.close()

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
