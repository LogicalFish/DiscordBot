import random
import re
import logging

from bot_identity.delayed_responses import DelayedResponder
from bot_identity.general_responses import GeneralResponder
from bot_identity.identity import Identity, IdentityError
from database.models.banned_channels_model import BannedChannel

from config import configuration, localization

id_config = configuration['identity']

logger = logging.getLogger(__name__)


class IdentityManager:
    """
    The manager for keeping track of identities and identity-related settings.
    Attributes:
        database (database_manager):
        identities (list): A list that should contain all identities.
        current_id (Identity): The current identity of the bot.
        verbose (bool): Whether the bot is currently allowed to speak or not.
        interval (int): the minimum interval in seconds between messages.
        banned_channels (list): List of channels where the bot is 'banned'.
    """

    def __init__(self, database_manager, reminder_manager=None):
        self.default_id = None
        self.identities = []
        self.initialize_identities()
        self.current_id = self.identities[0]

        self.verbose = id_config['default_verbose']
        self.interval = id_config['default_interval']
        self.banned_channels = []

        self.database = database_manager
        if self.database is not None:
            self.initialize_ban_list()
        if "facts_file" in id_config:
            fact_path = id_config['identity_dir'] + [id_config['facts_file']]
            if reminder_manager:
                self.responder = DelayedResponder(fact_path, reminder_manager)
            else:
                self.responder = GeneralResponder(fact_path)
        else:
            self.responder = None

    def initialize_identities(self):
        """
        A method for initialize all identities based on the settings.
        """
        self.default_id = Identity(id_config['identity_dir'] + [id_config['default_identity']], default=True)
        for file in configuration['identity']['identity_files']:
            try:
                new_identity = Identity(configuration['identity']['identity_dir'] + [file])
                self.identities.append(new_identity)
            except IdentityError as ie:
                logger.warning("IdentityError: {0} Skipping identity {1}.".format(ie, file))
                continue
            except FileNotFoundError:
                logger.warning("File {0} not found. Skipping identity {0}.".format(file))
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
            logger.info("Banning the following channel: {}".format(channel_id))
            if self.database is not None:
                self.database.insert(BannedChannel(channel_id))
            self.banned_channels.append(channel_id)
        else:
            raise ValueError("Can't ban a channel that is already banned.")

    def un_ban(self, channel_id):
        """Removes a channel from the banned list and logs the change."""
        if channel_id in self.banned_channels:
            logger.info("Unbanning the following channel: {}".format(channel_id))
            if self.database is not None:
                self.database.delete(BannedChannel, channel_id)
            self.banned_channels.remove(channel_id)
        else:
            raise ValueError("Can't unban a channel that is not banned.")

    def get_bans_string(self):
        """Returns a list of banned channels (if any)"""
        if len(self.banned_channels) == 0:
            return localization['bot_status']['not_banned']
        result = localization['bot_status']['banned']
        for channel_id in self.banned_channels:
            result += "<#{}>,".format(channel_id)
        return result[:-1]

    def get_verbosity_string(self):
        """Returns a string based on whether the bot is verbose or not."""
        return localization['bot_status']['verbose'] if self.verbose else localization['bot_status']['mute']

    def get_random_other_id(self):
        """Returns a random id (which is not the current id.)"""
        ex_id = self.identities.copy()
        ex_id.remove(self.current_id)
        return random.choice(ex_id)

    def get_current_ai(self):
        """Returns the current game difficulty of the bot."""
        return self.current_id.get_ai()

    def id_statement(self, category, tag):
        response = self.current_id.get_phrase(category, tag)
        if not response:
            response = self.default_id.get_phrase(category, tag)
        return response

    def get_identity_response(self, message):
        """
        Searches through a message and returns and phrases specific to the supplied identity
        :param message: The message to be searched through.
        :return: A random response based on the message, or an empty string if none could be found.
        """

        unique_triggers = self.current_id.get_unique_triggers()
        for phrase in unique_triggers:
            regex = unique_triggers[phrase].lower()
            matches = re.findall(regex, message.content.lower())
            if len(matches):
                response = self.current_id.get_phrase("unique", phrase)
                logger.info("Identity {} is responding to unique trigger '{}' with phrase: "
                            "'{}'".format(self.current_id, phrase, response))
                return response

        universal_triggers = id_config["universal_phrases"]
        for phrase in universal_triggers:
            regex = universal_triggers[phrase].format(bot_regex=self.current_id.regex).lower()
            matches = re.findall(regex, message.content.lower())
            if len(matches):
                response = self.id_statement("general", phrase)
                logger.info("Identity {} responding to universal trigger '{}' with phrase: "
                            "'{}'".format(self.current_id, phrase, response))
                return response

        if self.responder:
            generic_triggers = self.responder.get_triggers()
            for phrase in generic_triggers:
                regex = generic_triggers[phrase].lower()
                matches = re.findall(regex, message.content.lower())
                if len(matches):
                    response = self.responder.get_random_fact(phrase, message)
                    logger.info("Bot responding to generic trigger '{}' with phrase: '{}'".format(phrase, response))
                    return response

        return ""

    def find_new_id(self, message):
        """
        Method that goes through a message to find all identities that are mentioned within.

        :param message: The message sent by a user.
        :return: A list containing all the identities that have been mentioned in the text.
        """
        result = []
        for identity in self.identities:
            try:
                matches = re.findall(identity.regex.lower(), message.lower())
                if len(matches):
                    result.append(identity)
            except IdentityError as ie:
                logger.warning("IdentityError: {} Skipping identity.".format(ie))
        return result
