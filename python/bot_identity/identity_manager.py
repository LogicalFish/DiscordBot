import random

import config
from bot_identity.identity import Identity, IdentityError
from config import configuration
from database.models.banned_channels_model import BannedChannel


class IdentityManager:
    """
    The manager for keeping track of identities and identity-related settings.
    Attributes:
        database (database_manager):
        identities (list): A list that should contain all identities.
        current_id (Identity): The current identity of the bot.
        chatty (bool): Whether the bot is currently allowed to speak or not.
        interval (int): the minimum interval in seconds between messages.
        banned_channels (list): List of channels where the bot is 'banned'.
    """

    def __init__(self, database_manager):
        self.identities = []
        self.initialize_identities()
        self.current_id = self.identities[0]
        self.chatty = True
        self.interval = 0
        self.banned_channels = []
        self.database = database_manager
        if self.database is not None:
            self.initialize_ban_list()

    def initialize_identities(self):
        """
        A method for initialize all identities based on the settings.
        """
        for file in configuration['identity']['identity_files']:
            try:
                self.identities.append(Identity(file))
            except IdentityError as ie:
                print("IdentityError: {} Skipping identity {}.".format(ie, file))
                continue
            except FileNotFoundError:
                print("File {0} not found. Skipping identity {0}.".format(file))
                continue

    def initialize_ban_list(self):
        """
        Initializes the list of banned channels, taking from the database.
        DATABASE REQUIRED
        """
        channel_db = self.database.select_all(BannedChannel)
        self.banned_channels = [channel.channel_id for channel in channel_db]

    def ban(self, channel_id):
        """Adds a channel to the banned list and logs the change."""
        if channel_id not in self.banned_channels:
            print("Banning the following channel: {}".format(channel_id))
            if self.database is not None:
                self.database.insert(BannedChannel(channel_id))
            self.banned_channels.append(channel_id)
        else:
            raise ValueError("Can't ban a channel that is already banned.")

    def un_ban(self, channel_id):
        """Removes a channel from the banned list and logs the change."""
        if channel_id in self.banned_channels:
            print("Unbanning the following channel: {}".format(channel_id))
            if self.database is not None:
                self.database.delete(BannedChannel, channel_id)
            self.banned_channels.remove(channel_id)
        else:
            raise ValueError("Can't unban a channel that is not banned.")

    def get_bans_string(self):
        """Returns a list of banned channels (if any)"""
        if len(self.banned_channels) == 0:
            return config.localization['bot_status']['not_banned']
        result = config.localization['bot_status']['banned']
        for channel_id in self.banned_channels:
            result += "<#{}>,".format(channel_id)
        return result[:-1]

    def get_chatty_string(self):
        """Returns a string based on whether the bot is chatty or not."""
        if self.chatty:
            return config.localization['bot_status']['chatty']
        else:
            return config.localization['bot_status']['not_chatty']

    def get_random_other_id(self):
        """Returns a random id (which is not the current id.)"""
        ex_id = self.identities.copy()
        ex_id.remove(self.current_id)
        return random.choice(ex_id)

    def get_current_ai(self):
        """Returns the current game difficulty of the bot."""
        return self.current_id.get_AI()
