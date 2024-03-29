import logging
from bot_identity.identity_manager import IdentityManager
from database.database_connection import DatabaseError
from database.database_manager import DatabaseManager
from modules.birthday.birthday_manager import BirthdayManager
from modules.reminders.reminder_manager import ReminderManager

logger = logging.getLogger(__name__)


class SystemManager:
    """
    A Class that will help keep track of global variables related to the bot.

    Attributes:
        last_msg (int): Timing of the last message
        bot (User): The user object associated with the bot.
        ttt_games (dict): A dictionary of currently ongoing games.
    """

    def __init__(self, configuration):
        self.configuration = configuration
        self.last_msg = 0
        self.bot = None
        self.ttt_games = {}
        if self.configuration['database']['active']:
            try:
                self.database_manager = DatabaseManager()
            except DatabaseError as db_error:
                self.database_manager = None
                logger.warning("Error. {} Database functionality disabled.".format(str(db_error)))
        else:
            self.database_manager = None

        self.reminder_manager = ReminderManager()
        self.id_manager = IdentityManager(self.database_manager, self.reminder_manager)
        self.birthday_manager = BirthdayManager(self.database_manager)

        if self.database_manager and self.configuration['commands']['calendar']:
            from modules.calendar.event_manager import EventManager
            from modules.calendar.time_manager import TimeManager
            self.event_manager = EventManager(self.database_manager)
            self.time_manager = TimeManager(self.event_manager)
        else:
            self.event_manager = None
            self.time_manager = None

        if self.configuration['commands']['nicknames']:
            from modules.nicknames.nickname_manager import NicknameManager
            self.name_manager = NicknameManager(self.database_manager)
        else:
            from modules.nicknames.name_manager import NameManager
            self.name_manager = NameManager()

        if self.configuration['commands']['wheel']:
            from modules.games.wheel.wheel_manager import WheelManager
            self.wheel_manager = WheelManager(self.database_manager)
        else:
            self.wheel_manager = None

    @staticmethod
    async def get_user_by_id(user_id, client=None, guild=None):
        """
        Method for obtaining a name when all you have is an ID.
        :param user_id: The user ID
        :param client: The discord client. Required to fetch user objects based on ID.
        :param guild: The Guild the user is part of, if any.
        :return:
        """
        user = None
        if client:
            user = await client.fetch_user(user_id)
        elif guild:
            user = await guild.fetch_member(user_id)
        return user
