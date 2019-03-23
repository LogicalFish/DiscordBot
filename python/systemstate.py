
from commands.modules.calendar.clock_manager import TimeManager
from commands.modules.calendar.event_manager import EventManager
from database.db_manager import DatabaseManager
from responder.identity import Identity, IdentityError
import settings
import random

class System_State:
    """
    A Class that will help keep track of global variables related to the bot.

    Attributes:
        identities (list): A list containing all identities found in the settings.
        current_id (Identity): The current identity of the bot.
        chatty (bool): Whether the bot is currently speaking or not
        banned_channels (list): List of channels where the bot is 'banned'
        interval (int): the minimum interval in seconds between messages.
        last_msg (int): Timing of the last message
        bot (User): The user object associated with the bot.
        ttt_games (dict): A dictionary of currently ongoing games.
    """
    ttt_games = {}


    def __init__(self):
        self.identities = []
        for file in settings.IDENTITY_FILES:
            try:
                self.identities.append(Identity(settings.XML_DIR + file))
            except IdentityError as ie:
                print("IdentityError: {} Skipping identity {}.".format(ie, file))
                continue
            except FileNotFoundError as fnf:
                print("File {0} not found. Skipping identity {0}.".format(file))
                continue
        self.current_id = self.identities[0]
        self.chatty = True
        self.banned_channels = []
        self.interval = 0
        self.last_msg = 0
        self.bot = None
        self.nicknames = {}
        self.db_man = DatabaseManager()
        self.event_man = EventManager(self.db_man)
        self.tim_man = TimeManager(self.event_man)

    # def change_id(self, identity):
    #     self.current_id = identity

    def ban(self, channel):
        """Adds a channel to the banned list and logs the change."""
        print("Banning the following channel: {}".format(channel))
        self.banned_channels.append(channel)

    def unban(self, channel):
        """Removes a channel from the banned list and logs the change."""
        print("Unbanning the following channel: {}".format(channel))
        self.banned_channels.remove(channel)

    def get_bans(self):
        """Returns a list of banned channels (if any)"""
        if len(self.banned_channels) == 0:
            #"banned nowhere"
            return "Nergens verbannen"
        #"banned in"
        result = "Verbannen in "
        for channel in self.banned_channels:
            result += "#{},".format(channel.name)
        return result[:-1]

    def chatty_str(self):
        """Returns a string based on whether the bot is chatty or not."""
        if self.chatty:
            #"chatty"
            return "spraakzaam"
        else:
            #"silent"
            return "stil"

    def get_random_other_id(self):
        """Returns a random id (which is not the current id.)"""
        ex_id = self.identities.copy()
        ex_id.remove(self.current_id)
        return random.choice(ex_id)

    def get_current_ai(self):
        """Returns the current game difficulty of the bot."""
        return self.current_id.get_AI()

    def get_name(self, user):
        if user in self.nicknames:
            return self.nicknames[user]
        if user.nick != None:
            return user.nick
        else:
            return user.name
