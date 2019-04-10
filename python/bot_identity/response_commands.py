from commands.command_superclass import Command
from commands.command_error import CommandError
from bot_identity import parser


class StatusCommand(Command):
    def __init__(self):
        call = ["status"]
        parameters = "None."
        description = "Inquire about the current chat-status of the bot."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        return {"response": self.get_status(system.id_manager)}

    @staticmethod
    def get_status(id_manager):
        return parser.direct_call(id_manager.current_id, "status").format(id_manager.get_chatty_string(),
                                                                          id_manager.get_bans_string().lower(),
                                                                          id_manager.interval)


class BanCommand(Command):
    def __init__(self):
        call = ["ban"]
        parameters = "None."
        description = "This command will ban the bot from chatting in the current channel."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        try:
            system.id_manager.ban(message.channel.id)
            return {"response": parser.direct_call(system.id_manager.current_id, "leave")}
        except ValueError as error:
            raise CommandError(str(error), None)


class UnBanCommand(Command):
    def __init__(self):
        call = ["unban"]
        parameters = "None."
        description = "This command will allow the bot to chat in the current channel."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        try:
            system.id_manager.un_ban(message.channel.id)
            return {"response": parser.direct_call(system.id_manager.current_id, "call")}
        except ValueError as error:
            raise CommandError(str(error), None)


class ChatToggleCommand(Command):
    def __init__(self):
        call = ["chat", "chatty"]
        parameters = "*(optional)* T(rue) or Y(es) to allow all chat. F(alse) or N(o) to suppress all chat."
        description = "This function will suppress or allow all bot chat functions."
        super().__init__(call, parameters, description)

    def in_call(self, command):
        return command.startswith(self.call[0])

    def execute(self, param, message, system):
        i = self.translate_param(param)
        if not system.id_manager.chatty and i != 0:
            system.id_manager.chatty = True
            return {"response": parser.direct_call(system.id_manager.current_id, "chatty")}
        elif system.id_manager.chatty and i != 1:
            system.id_manager.chatty = False
            return {"response": parser.direct_call(system.id_manager.current_id, "nonchatty")}
        else:
            return {"response": StatusCommand.get_status(system.id_manager)}

    @staticmethod
    def translate_param(param):
        if param.lower().startswith("t") or param.lower().startswith("y"):
            return 1
        if param.lower().startswith("f") or param.lower().startswith("n"):
            return 0
        else:
            return -1


class IntervalCommand(Command):
    def __init__(self):
        call = ["interval"]
        parameters = "An integer representing the seconds between response."
        description = "This function will disallow the bot to chat for the amount of seconds supplied."
        super().__init__(call, parameters, description)

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
                return {"response": parser.direct_call(identities.current_id, "nonchatty")}
            else:
                return {"response": parser.direct_call(identities.current_id, "chatty")}

        except ValueError:
            raise CommandError("number_not_valid", param)


class LeaveCommand(Command):
    def __init__(self):
        call = ["leave"]
        parameters = "None."
        description = "This function swaps the current identity out for a new, random one."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        return {"leave": system.id_manager.get_random_other_id()}

