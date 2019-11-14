from bot_identity.identity_manager import IdentityManager
from database.database_manager import DatabaseManager
from modules.calendar.event_manager import EventManager
from modules.calendar.time_manager import TimeManager
from modules.games.wheel.wheel_manager import WheelManager
from modules.nicknames.nickname_manager import NicknameManager
from modules.birthday.birthday_manager import BirthdayManager
from modules.reminders.reminder_manager import ReminderManager


class SystemManager:
    """
    A Class that will help keep track of global variables related to the bot.

    Attributes:
        last_msg (int): Timing of the last message
        bot (User): The user object associated with the bot.
        ttt_games (dict): A dictionary of currently ongoing games.
    """

    def __init__(self):
        self.last_msg = 0
        self.bot = None
        self.ttt_games = {}
        self.database_manager = DatabaseManager()
        if self.database_manager.db.engine is not None:
            self.event_manager = EventManager(self.database_manager)
            self.time_manager = TimeManager(self.event_manager)
        else:
            self.database_manager = None
            self.event_manager = None
            self.time_manager = None
        self.id_manager = IdentityManager(self.database_manager)
        self.nickname_manager = NicknameManager(self.database_manager)
        self.birthday_manager = BirthdayManager(self.database_manager)
        self.wheel_manager = WheelManager(self.database_manager)
        self.reminder_manager = ReminderManager()
