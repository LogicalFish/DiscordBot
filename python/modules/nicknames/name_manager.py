class NameManager:

    def get_name(self, user):
        """
        Returns a user's name. Returns their display name if they have no nickname.
        :param user: The user object whose name you want.
        :return: The user's nickname, or display name if no nickname is found.
        """
        return user.display_name
