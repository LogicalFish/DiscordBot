import random
import settings

from responder.identity import Identity, IdentityError

BAN_TABLE = "banned_channels"
PRIMARY_KEY = "channel_id"


class IdentityManager:
    """
    Attributes:
        identities (list): A list containing all identities found in the settings.
        current_id (Identity): The current identity of the bot.
        chatty (bool): Whether the bot is currently speaking or not
        banned_channels (list): List of channels where the bot is 'banned'
        interval (int): the minimum interval in seconds between messages.
    """

    def __init__(self, database_manager):
        self.database = database_manager
        self.identities = []
        self.initialize_identities()
        self.current_id = self.identities[0]
        self.chatty = True
        self.interval = 0
        self.banned_channels = []
        self.initialize_ban_list()

    def initialize_identities(self):
        for file in settings.IDENTITY_FILES:
            try:
                self.identities.append(Identity(settings.XML_DIR + file))
            except IdentityError as ie:
                print("IdentityError: {} Skipping identity {}.".format(ie, file))
                continue
            except FileNotFoundError:
                print("File {0} not found. Skipping identity {0}.".format(file))
                continue

    def initialize_ban_list(self):
        rows = self.database.get_rows(BAN_TABLE, sort=PRIMARY_KEY)
        self.banned_channels = [row[0] for row in rows]

    def ban(self, channel_id):
        """Adds a channel to the banned list and logs the change."""
        if channel_id not in self.banned_channels:
            print("Banning the following channel: {}".format(channel_id))
            self.database.insert({PRIMARY_KEY: channel_id}, BAN_TABLE)
            self.banned_channels.append(channel_id)
        else:
            raise ValueError("Can't ban a channel that is already banned.")

    def un_ban(self, channel_id):
        """Removes a channel from the banned list and logs the change."""
        if channel_id in self.banned_channels:
            print("Unbanning the following channel: {}".format(channel_id))
            self.database.delete("'{}'".format(channel_id), PRIMARY_KEY, BAN_TABLE)
            self.banned_channels.remove(channel_id)
        else:
            raise ValueError("Can't unban a channel that is not banned.")

    def get_bans_string(self):
        """Returns a list of banned channels (if any)"""
        if len(self.banned_channels) == 0:
            # "banned nowhere"
            return "Nergens verbannen"
        # "banned in"
        result = "Verbannen in "
        for channel_id in self.banned_channels:
            result += "<#{}>,".format(channel_id)
        return result[:-1]

    def get_chatty_string(self):
        """Returns a string based on whether the bot is chatty or not."""
        if self.chatty:
            # "chatty"
            return "spraakzaam"
        else:
            # "silent"
            return "stil"

    def get_random_other_id(self):
        """Returns a random id (which is not the current id.)"""
        ex_id = self.identities.copy()
        ex_id.remove(self.current_id)
        return random.choice(ex_id)

    def get_current_ai(self):
        """Returns the current game difficulty of the bot."""
        return self.current_id.get_AI()
