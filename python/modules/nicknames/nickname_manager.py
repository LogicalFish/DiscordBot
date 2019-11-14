from database.models.nicknames_model import Nickname


class NicknameManager:

    """
    Class that can keep track of user's nicknames. This way, they can decide what the bot calls them.
    Uses a database for storing nicknames.
    """

    def __init__(self, database_manager):
        self.database = database_manager
        self.nicknames = {}
        if self.database is not None:
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
        nickname_db = self.database.select_all(Nickname)
        for nickname in nickname_db:
            self.nicknames[nickname.user_id] = nickname.nickname

    def add_nickname(self, user_id, nickname):
        """
        Adds a nickname
        :param user_id: The user_id of the user whose nickname you are adding.
        :param nickname: The nickname the user wishes to have.
        :return:
        """
        if self.database is not None:
            session = self.database.Session()
            current_nick = session.query(Nickname).filter(Nickname.user_id == user_id).first()
            if current_nick:
                current_nick.nickname = nickname
            else:
                session.add(Nickname(user_id, nickname))
            session.commit()
            session.close()
        self.nicknames[user_id] = nickname

    def get_name_by_id(self, user_id, client, guild=None):
        """
        Method for obtaining a name when all you have is an ID.
        :param user_id: The user ID
        :param client: The discord client. Required to fetch user objects based on ID.
        :param guild: The Guild the user is part of, if any.
        :return:
        """
        if user_id in self.nicknames:
            return self.nicknames[user_id]
        if guild:
            return guild.get_member(user_id).display_name
        return client.get_user(user_id).display_name
