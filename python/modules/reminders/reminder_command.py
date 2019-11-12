import re

from datetime import timedelta

from bot_identity import parser
from commands.command_error import CommandError
from commands.command_superclass import Command


class RemindCommand(Command):

    def __init__(self):
        call = ["remindme", "reminder"]
        parameters = "Two variables: The first how far into the future you would like to be reminded. " \
                     "(Example: 30m(inutes) , 2 uur , up to days). The second is the message to remind you of."
        description = "A helpful tool to remind you in the future of a thing you thought of just now!"
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        dissection = re.findall("(\\d+)\\s?([a-zA-Z])\\w*\\s+(.*)", param)
        if dissection:
            time_str, unit, text = dissection[0]
            try:
                time = int(time_str)
                delta = get_delta(time, unit)
                system.reminder_manager.add_reminder(delta, "> " + text, message.author)
                return {"response": parser.direct_call(system.id_manager.current_id, "reminder")}
            except ValueError:
                raise CommandError("number_not_valid", time_str)
        else:
            raise CommandError("invalid_reminder", param)

    def in_call(self, command):
        if command.startswith("remind"):
            return True
        return False


def get_delta(time, unit):
    if unit == "s":
        return timedelta(seconds=time)
    if unit == "m":
        return timedelta(minutes=time)
    if unit == "h" or unit == "u":
        return timedelta(hours=time)
    if unit == "d":
        return timedelta(days=time)
