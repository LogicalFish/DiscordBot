from commands.command_superclass import Command
from commands.command_error import CommandError


class StatusCommand(Command):
    """
    Command for responding with the bot's (identity manager) status, including banned channels and chat intervals.
    """

    def __init__(self):
        super().__init__('bot_status')

    def execute(self, param, message, system):
        return {"response": self.get_status(system.id_manager)}

    @staticmethod
    def get_status(id_manager):
        """Method for getting the status string. Can be used by other classes if necessary."""
        return id_manager.id_statement("general", "status").format(id_manager.get_verbosity_string(),
                                                                   id_manager.get_bans_string().lower(),
                                                                   id_manager.interval)


class BanCommand(Command):
    """
    Command for banning the bot's response module from responding from the current channel.
    """

    def __init__(self):
        super().__init__('ban')

    def execute(self, param, message, system):
        try:
            system.id_manager.ban(message.channel.id)
            return {"response": system.id_manager.id_statement("general", "leave")}
        except ValueError:
            raise CommandError("already_banned", None)


class UnBanCommand(Command):
    """
    Command for unbanning the bot's response module from the current channel.
    """

    def __init__(self):
        super().__init__('unban')

    def execute(self, param, message, system):
        try:
            system.id_manager.un_ban(message.channel.id)
            return {"response": system.id_manager.id_statement("general", "call")}
        except ValueError:
            raise CommandError("not_banned", None)


class ChatToggleCommand(Command):
    """
    Command for toggling the bot's response module.
    """

    def __init__(self):
        super().__init__('chattoggle')

    def in_call(self, command):
        return command.startswith(self.call[0])

    def execute(self, param, message, system):
        param_bool = self.translate_param(param)
        if not system.id_manager.verbose and param_bool is not False:
            system.id_manager.verbose = True
            return {"response": system.id_manager.id_statement("general", "chatty")}
        elif system.id_manager.verbose and param_bool is not True:
            system.id_manager.verbose = False
            return {"response": system.id_manager.id_statement("general", "nonchatty")}
        else:
            return {"response": StatusCommand.get_status(system.id_manager)}

    @staticmethod
    def translate_param(param):
        """
        Helper method for deciding whether a parameter corresponds to true or false.
        :param param: The parameter.
        :return: boolean: Whether or not the parameter corresponds to True, False, or neither.
        """
        if param.lower().startswith("t") or param.lower().startswith("y"):
            return True
        if param.lower().startswith("f") or param.lower().startswith("n"):
            return False
        return None


class IntervalCommand(Command):
    """
    Command for changing the interval at which the bot is allowed to send messages.
    """

    def __init__(self):
        super().__init__('interval')

    def execute(self, param, message, system):
        """
        A method for changing the chat interval of the bot.
        :param param: The parameter string. Should contain only an integer.
        :param message: Unused parent parameter.
        :param system: The system meta-object, containing information about the current state of the bot.
        :return: A response that signifies whether the bot will speak more often or less often.
        """
        identities = system.id_manager
        try:
            old_val = identities.interval
            identities.interval = int(param)
            print("Changing the interval from {} to {}".format(old_val, identities.interval))
            if old_val == identities.interval:
                return {"response": StatusCommand.get_status(identities)}
            elif old_val < identities.interval:
                return {"response": system.id_manager.id_statement("general", "nonchatty")}
            else:
                return {"response": system.id_manager.id_statement("general", "chatty")}

        except ValueError:
            raise CommandError("number_not_valid", param)


class DismissCommand(Command):
    """
    Command for randomly selecting another bot persona.
    """

    def __init__(self):
        super().__init__('dismiss')

    def execute(self, param, message, system):
        return {"leave": system.id_manager.get_random_other_id()}
