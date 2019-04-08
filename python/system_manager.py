from commands.modules.calendar.time_manager import TimeManager
from commands.modules.calendar.event_manager import EventManager
from commands.modules.nicknames.nickname_manager import NicknameManager
from database.database_manager import DatabaseManager
from responder.identity_manager import IdentityManager


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
        self.id_manager = IdentityManager(self.database_manager)
        self.event_manager = EventManager(self.database_manager)
        self.time_manager = TimeManager(self.event_manager)
        self.nickname_manager = NicknameManager(self.database_manager)
