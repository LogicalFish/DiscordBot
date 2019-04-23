import re
import settings
from commands.command_superclass import Command
from modules.calendar import shadow_events, event_reader
from modules.calendar.event_model import EventError
from commands.command_error import CommandError


class EventCommand(Command):
    """
    Command class for Reading an event.
    """

    def __init__(self):
        call = ["event"]
        parameters = "The Event ID of the event you wish to show."
        description = "Show details of the event."
        super().__init__(call, parameters, description)

    def execute(self, param, message, system):
        """
        Accepts a single digit as parameter.
        :param param: A single digit representing the Event ID. Throws an error otherwise.
        :param message: Unused parameter.
        :param system: Used to call the event_manager.
        :return: An Embed with the event-data within it.
        """
        if system.event_manager is None:
            raise CommandError("database_error", None)
        try:
            event_id = int(param)
            event = system.event_manager.get_event(event_id)
            if event:
                embed = event_reader.get_event_embed(event)
            else:
                raise CommandError("event_not_found", param)
        except ValueError:
            raise CommandError("number_not_valid", param)
        return {"event_embed": (embed, event["author"])}


class ListEventCommand(Command):
    """
    Command class for listing all events, including future recurring events.
    """

    def __init__(self):
        call = ["events", "listevents"]
        parameters = "The amount of 'shadow' events should be shown."
        description = "A list of all events."
        super().__init__(call, parameters, description)

    def in_call(self, command):
        if "events" in command or ("list" in command and "event" in command):
            return True
        return False

    def execute(self, param, message, system):
        if system.event_manager is None:
            raise CommandError("database_error", None)
        try:
            shadow_size = int(param)
        except ValueError:
            shadow_size = settings.DEFAULT_SHADOW
        events_list = system.event_manager.get_all_events()
        shadow_list = shadow_events.get_list_shadow(events_list, shadow_size)
        list_message = "De volgende evenementen zijn gepland:\n\n"
        for date, shadow_message in shadow_list:
            if len(list_message) + len(shadow_message) < 2000:
                list_message += shadow_message
        if not events_list:
            list_message = "Er zijn geen evenementen gevonden."
        return {"response": list_message}


class CreateEventCommand(Command):
    """
    Command class for Creating an event.
    """

    def __init__(self):
        call = ["eventadd", "eventcreate"]
        parameters = '\n\t\t*Name*: The name of the event. *(required.)*\n' \
                     '\t\t*Date*: The date and time this event takes place. *(required.)*\n' \
                     '\t\t*Description*: A description of the event.\n' \
                     '\t\t*Reminder*: The times in hours, separated by commas, when you want to show reminders.\n' \
                     '\t\t*Tag*: The role you wish to tag during reminders.\n' \
                     '\t\t*Channel*: The channel you wish to show reminders in. Current channel is the default.\n' \
                     '\t\t*Recur*: Integer designating in how many days event will reoccur after the last. ' \
                     'If not supplied, event does not reoccur.\n'
        description = 'Creates a new event based on the supplied parameters. ' \
                      '\n\t\tExample: *{}createdate name="Christmas" date="December 25th"*'.format(settings.SIGN)
        super().__init__(call, parameters, description)

    def in_call(self, command):
        if "event" in command and ("add" in command or "create" in command):
            return True
        return False

    def execute(self, param, message, system):
        if system.event_manager is None:
            raise CommandError("database_error", None)
        try:
            event_dict = system.event_manager.model.create_event_dict(param)
            system.event_manager.model.clean_data(event_dict)
            event_dict[system.event_manager.model.key_author] = message.author.id
            if "channel" not in event_dict.keys():
                event_dict["channel"] = message.channel.name
            event = system.event_manager.create_event(event_dict)
            return {"response": "Created event {}:".format(event[system.event_manager.model.PRIMARY_KEY]),
                    "event_embed": (event_reader.get_event_embed(event), event["author"])}
        except EventError as error:
            raise CommandError(error.message, error.parameters)


class EditEventCommand(Command):
    """
    Command class for Updating an event
    """

    def __init__(self):
        call = ["eventedit", "eventupdate"]
        parameters = "\n\t*id*: The ID of the event you wish to edit. *(required)*\n" \
                     "\tSee {}eventadd for other parameters.".format(settings.SIGN)
        description = "Edits the parameters of a given event."
        super().__init__(call, parameters, description)

    def in_call(self, command):
        if "event" in command and ("edit" in command or "update" in command):
            return True
        return False

    def execute(self, param, message, system):
        if system.event_manager is None:
            raise CommandError("database_error", None)
        event_dict = system.event_manager.model.create_event_dict(param)
        if "id" in event_dict:
            id_str = event_dict["id"]
        else:
            id_str = param.split(' ', 1)[0]
        try:
            event_id = int(id_str)
        except ValueError:
            raise CommandError("number_not_valid", id_str)
        try:
            system.event_manager.model.clean_data(event_dict)
            event = system.event_manager.update_event(event_id, event_dict, message.author.id)
            return {"response": "Updated event {}:".format(event_id),
                    "event_embed": (event_reader.get_event_embed(event), event["author"])}
        except EventError as error:
            raise CommandError(error.message, error.parameters)


class DeleteEventCommand(Command):
    """
    Command class for Deleting an event.
    """

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
        if system.event_manager is None:
            raise CommandError("database_error", None)
        try:
            event_id = int(param)
            event_name = system.event_manager.delete_event(event_id, message.author.id)
            response = "Event {}: {} deleted.".format(event_id, event_name)
        except ValueError:
            raise CommandError("number_not_valid", param)
        except EventError as error:
            raise CommandError(error.message, error.parameters)
        return {"response": response}


class UnShadowCommand(Command):
    """
    Command class for allowing an event's shadow to be edited.
    """

    def __init__(self):
        call = ["unshadow", "revealevent", "deshadow"]
        parameters = "The Event ID of the shadow event you wish to access. Example: 1-2."
        description = "Makes the shadow of an event accessible."
        super().__init__(call, parameters, description)

    def in_call(self, command):
        if "shadow" in command:
            return True
        elif "reveal" in command and "event" in command:
            return True
        return False

    def execute(self, param, message, system):
        if system.event_manager is None:
            raise CommandError("database_error", None)
        try:
            parameter_match = re.search("(\\d+)-(\\d+)", param.replace(" ", ""))
            if parameter_match is None:
                raise CommandError("event_not_found", param)
            event_id = int(parameter_match[1])
            shadow_id = int(parameter_match[2])
            if 0 < shadow_id < settings.MAX_SHADOW:
                for i in range(shadow_id+1):
                    new_event = system.event_manager.pop_event(event_id, message.author.id)
            else:
                raise CommandError("invalid_shadow", param)

            response = event_reader.get_reveal_message(param, new_event[system.event_manager.model.PRIMARY_KEY])
        except EventError as error:
            raise CommandError(error.message, error.parameters)
        return {"response": response}
