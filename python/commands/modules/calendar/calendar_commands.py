import settings
from commands.command_superclass import Command
from commands.modules.calendar import event_reader, shadow_events
from commands.modules.calendar.event_model import EventError


class EventCommand(Command):

    def __init__(self):
        call = ["event"]
        parameters = "The Event ID of the event you wish to show."
        description = "Show details of the event."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        try:
            event_id = int(param)
            event = system.event_manager.get_event(event_id)
            if event:
                response = event_reader.describe_long(event)
            else:
                response = "[ERROR]: Geen event met ID '{}' gevonden.".format(param)
        except ValueError:
            response = "[ERROR]: ID '{}' is geen valide ID.".format(param)
        return {"response": response}


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
        try:
            shadow_size = int(param)
        except ValueError:
            shadow_size = 4
        events_list = system.event_manager.get_all_events()
        shadow_list = shadow_events.get_list_shadow(events_list, shadow_size)
        list_message = ""
        for date, shadow_message in shadow_list:
            list_message += shadow_message
        if not events_list:
            list_message = "Er zijn geen evenementen gevonden."
        return {"response": list_message}


class CreateEventCommand(Command):

    def __init__(self):
        call = ["eventadd", "eventcreate"]
        parameters = '\n\t\t*Name*: The name of the event. *(required.)*\n' \
                     '\t\t*Date*: The date and time this event takes place. *(required.)*\n' \
                     '\t\t*Description*: A description of the event.\n' \
                     '\t\t*Reminder*: The times in hours, separated by commas, when you want to show reminders.\n' \
                     '\t\t*Tag*: The role you wish to tag during reminders.\n' \
                     '\t\t*Channel*: The channel you wish to show reminders in. Current channel is the default.\n' \
                     '\t\t*Recurring*: Integer designating in how many days event will reoccur after the last. ' \
                     'If not supplied, event does not reoccur.\n' \
                     '\t\t*Multiply*: Two integers in the format *"*X,+Y"*. ' \
                     '*X* designates how many events are created. ' \
                     '*Y* designates how many days apart each created event is.\n'
        description = 'Creates a new event based on the supplied parameters. ' \
                      '\n\t\tExample: *{}createdate name="Christmas" date="December 25th"*'.format(settings.SIGN)
        super().__init__(call, parameters, description)

    def in_call(self, command):
        if "event" in command and ("add" in command or "create" in command):
            return True
        return False

    def execute(self, param, message, system):
        try:
            event_dict = event_reader.create_event_dict(param)
            system.event_manager.model.clean_data(event_dict)
            event_dict[system.event_manager.model.key_author] = message.author.id
            if "channel" not in event_dict.keys():
                event_dict["channel"] = message.channel.name
            event = system.event_manager.create_event(event_dict)
            return {"response": "Created event {}:\n{}".format(event[system.event_manager.model.PRIMARY_KEY],
                                                               event_reader.describe_long(event))}
        except EventError as error:
            return {"response": "[ERROR]: {}".format(error)}


class EditEventCommand(Command):

    def __init__(self):
        call = ["eventedit", "eventupdate"]
        parameters = "\t**id**: The ID of the event you wish to edit. *(required)*\n" \
                     "\tSee {}eventadd for other parameters.".format(settings.SIGN)
        description = "Edits the parameters of a given event."
        super().__init__(call, parameters, description)

    def in_call(self, command):
        if "event" in command and ("edit" in command or "update" in command):
            return True
        return False

    def execute(self, param, message, system):
        event_dict = event_reader.create_event_dict(param)
        if "id" in event_dict:
            id_str = event_dict["id"]
        else:
            id_str = param.split(' ', 1)[0]
        try:
            identifier = int(id_str)
        except ValueError:
            return {"response": "[ERROR]: Id '{}' is geen valide ID.".format(id_str)}
        try:
            system.event_manager.model.clean_data(event_dict)
            event = system.event_manager.update_event(identifier, event_dict, message.author.id)
            return {"response": "Updated event {}:\n{}".format(identifier, event_reader.describe_long(event))}
        except EventError as error:
            return {"response": "[ERROR]: {}".format(error)}


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
        try:
            event_id = int(param)
            response = system.event_manager.delete_event(event_id, message.author.id)
        except ValueError:
            response = "[ERROR]: ID '{}' is geen valide ID.".format(param)
        except EventError as error:
            response = "[ERROR]: {}".format(error)
        return {"response": response}
