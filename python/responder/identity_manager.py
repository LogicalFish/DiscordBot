import random
import settings

from responder.identity import Identity, IdentityError


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

        self.identities = []
        for file in settings.IDENTITY_FILES:
            try:
                self.identities.append(Identity(settings.XML_DIR + file))
            except IdentityError as ie:
                print("IdentityError: {} Skipping identity {}.".format(ie, file))
                continue
            except FileNotFoundError:
                print("File {0} not found. Skipping identity {0}.".format(file))
                continue
        self.current_id = self.identities[0]
        self.chatty = True
        self.interval = 0
        self.banned_channels = []

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
            # "banned nowhere"
            return "Nergens verbannen"
        # "banned in"
        result = "Verbannen in "
        for channel in self.banned_channels:
            result += "#{},".format(channel.name)
        return result[:-1]

    def chatty_str(self):
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
