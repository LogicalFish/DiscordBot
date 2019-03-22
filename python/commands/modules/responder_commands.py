from commands.command import Command
from responder import parser


class StatusCommand(Command):
    def __init__(self):
        call = ["status"]
        parameters = "None."
        description = "Inquire about the current chat-status of the bot."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        return {"response": self.get_status(system)}

    @staticmethod
    def get_status(system):
        return parser.direct_call(system.current_id, "status").format(system.chatty_str(),
                                                                      system.get_bans().lower(),
                                                                      system.interval)


class BanCommand(Command):
    def __init__(self):
        call = ["ban"]
        parameters = "None."
        description = "This command will ban the bot from chatting in the current channel."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        system.ban(message.channel)
        return {"response": parser.direct_call(system.current_id, "leave")}


class UnbanCommand(Command):
    def __init__(self):
        call = ["unban"]
        parameters = "None."
        description = "This command will allow the bot to chat in the current channel."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        system.unban(message.channel)
        return {"response": parser.direct_call(system.current_id, "call")}


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
        if not system.chatty and i != 0:
            system.chatty = True
            return {"response": parser.direct_call(system.current_id, "chatty")}
        elif system.chatty and i != 1:
            system.chatty = False
            return {"response": parser.direct_call(system.current_id, "nonchatty")}
        else:
            return {"response": StatusCommand.get_status(system)}

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
        try:
            old_val = system.interval
            system.interval = int(param)
            print("Changing the interval from {} to {}".format(old_val, system.interval))
            if old_val == system.interval:
                return {"response": StatusCommand.get_status(system)}
            elif old_val < system.interval:
                return {"response": parser.direct_call(system.current_id, "nonchatty")}
            else:
                return {"response": parser.direct_call(system.current_id, "chatty")}

        except ValueError:
            return {"response": parser.direct_call(system.current_id, "error")}


class LeaveCommand(Command):
    def __init__(self):
        call = ["leave"]
        parameters = "None."
        description = "This function swaps the current identity out for a new, random one."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        return {"leave": system.get_random_other_id()}

