import settings
from commands.command import Command


class EventCommand(Command):

    def __init__(self):
        call = ["event"]
        parameters = "The Event ID of the event you wish to show."
        description = "Show details of the event."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        return {"response": system.event_man.show_event(param)}


class ListEventCommand(Command):

    def __init__(self):
        call = ["events", "listevents"]
        parameters = "None."
        description = "A list of all events."
        super().__init__(call, parameters, description)

    def in_call(self, command):
        if "events" in command or ("list" in command and "event" in command):
            return True
        return False

    def execute(self, param, message, system):
        return {"response": system.event_man.list_events()}


class CreateEventCommand(Command):

    def __init__(self):
        call = ["eventadd", "eventcreate"]
        parameters = '\n\t\t*Name*: The name of the event. *(required.)*\n' \
                     '\t\t*Date*: The date this event takes place. *(required.)*\n' \
                     '\t\t*Description*: A description of the event.\n' \
                     '\t\t*Reminder*: The times in hours, separated by commas, when you want to show reminders.\n' \
                     '\t\t*Tag*: The role you wish to tag during reminders.\n' \
                     '\t\t*Channel*: The channel you wish to show reminders in. Current channel is the default.\n' \
                     '\t\t*Recurring*: Integer designating in how many days event will reoccur after the last. ' \
                     'If not supplied, event does not reoccur.\n' \
                     '\t\t*Multiply*: Two integers in the format *"*X,+Y"*. *X* designates how many events are created. ' \
                     '*Y* designates how many days apart each created event is.\n'
        description = 'Creates a new event based on the supplied parameters. ' \
                      '\n\t\tExample: *{}createdate name="Christmas" date="December 25th"*'.format(settings.SIGN)
        super().__init__(call, parameters, description)

    def in_call(self, command):
        if "event" in command and ("add" in command or "create" in command):
            return True
        return False

    def execute(self, param, message, system):
        return {"response": system.event_man.create_event(param, message.author, message.channel.name)}


class EditEventCommand(Command):

    def __init__(self):
        call = ["eventedit"]
        parameters = "\t**id**: The ID of the event you wish to edit. *(required)*\n" \
                     "\tSee {}eventadd for other parameters.".format(settings.SIGN)
        description = "Edits the parameters of a given event."
        super().__init__(call, parameters, description)

    def in_call(self, command):
        if "event" in command and "edit" in command:
            return True
        return False

    def execute(self, param, message, system):
        return {"response": system.event_man.edit_event(param, message.author)}


class DeleteEventCommand(Command):

    def __init__(self):
        call = ["eventdelete"]
        parameters = "The Event ID of the event you wish to delete."
        description = "Deletes a given event."
        super().__init__(call, parameters, description)

    def in_call(self, command):
        if "event" in command and "delete" in command:
            return True
        return False

    def execute(self, param, message, system):
        return {"response": system.event_man.delete_event(param, message.author)}
