

NAME_TABLE = "nicknames"
PRIMARY_KEY = "user_id"
SECONDARY = "nickname"


class NicknameManager:

    def __init__(self, database_manager):
        self.database = database_manager
        self.nicknames = {}
        self.initialize_nicknames()

    def get_name(self, user):
        if user.id in self.nicknames:
            return self.nicknames[user.id]
        if user.nick is not None:
            return user.nick
        else:
            return user.name

    def initialize_nicknames(self):
        rows = self.database.get_rows(NAME_TABLE)
        for row in rows:
            self.nicknames[row[0]] = row[1]

    def add_nickname(self, user_id, nickname):
        if user_id in self.nicknames.keys():
            self.database.update({SECONDARY: nickname}, "'{}'".format(user_id), PRIMARY_KEY, NAME_TABLE)
        else:
            self.database.insert({PRIMARY_KEY: user_id, SECONDARY: nickname}, NAME_TABLE)
        self.nicknames[user_id] = nickname
