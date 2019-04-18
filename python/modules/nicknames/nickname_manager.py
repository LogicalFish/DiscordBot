

NAME_TABLE = "nicknames"
PRIMARY_KEY = "user_id"
SECONDARY = "nickname"


class NicknameManager:

    """
    Class that can keep track of user's nicknames. This way, they can decide what the bot calls them.
    Uses a database for storing nicknames.
    """

    def __init__(self, database_manager):
        self.database = database_manager
        self.nicknames = {}
        self.initialize_nicknames()

    def get_name(self, user):
        """
        Returns a user's name. Returns their display name if they have no nickname.
        :param user: The user object whose name you want.
        :return: The user's nickname, or display name if no nickname is found.
        """
        if user.id in self.nicknames:
            return self.nicknames[user.id]
        return user.display_name

    def initialize_nicknames(self):
        """
        Initializes the data within the class, reading it from a database.
        """
        rows = self.database.get_rows(NAME_TABLE)
        for row in rows:
            self.nicknames[row[0]] = row[1]

    def add_nickname(self, user_id, nickname):
        """
        Adds a nickname
        :param user_id: The user_id of the user whose nickname you are adding.
        :param nickname: The nickname the user wishes to have.
        :return:
        """
        if user_id in self.nicknames.keys():
            self.database.update({SECONDARY: nickname}, "'{}'".format(user_id), PRIMARY_KEY, NAME_TABLE)
        else:
            self.database.insert({PRIMARY_KEY: user_id, SECONDARY: nickname}, NAME_TABLE)
        self.nicknames[user_id] = nickname

    def get_name_from_id(self, user_id, client, guild=None):
        """
        Method for obtaining a name when all you have is an ID.
        :param user_id: The user ID
        :param client: The discord client. Required to fetch user objects based on ID.
        :param guild: The Guild the user is part of, if any.
        :return:
        """
        if guild:
            user_object = guild.get_member(user_id)
        else:
            user_object = client.get_user(user_id)
        return self.get_name(user_object)
