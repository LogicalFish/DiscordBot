import re
import config
import logging

from commands.command_error import CommandError
from commands.command_superclass import Command
from database.models.event_model import Event
from modules.calendar import event_parser
from modules.calendar.event_parser import EventError

logger = logging.getLogger("modules.calendar.commands")


class EventCommand(Command):
    """
    Command class for Reading an event.
    """

    def __init__(self):
        super().__init__('show_event')

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
                return {"embed": event.get_event_embed(),
                        "add_id": event.author}
            else:
                raise CommandError("event_not_found", param)

        except ValueError:
            raise CommandError("number_not_valid", param)


class ListEventCommand(Command):
    """
    Command class for listing all events, including future recurring events.
    """
    calendar_config = config.configuration['calendar']

    def __init__(self):
        super().__init__('list_events')
        self.parameters = self.parameters.format(self.calendar_config['default_shadow'])

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
            shadow_size = self.calendar_config['default_shadow']

        events_list = system.event_manager.get_all_events()
        if events_list:
            shadow_list = self.get_list_shadow(events_list, shadow_size)
            list_message = config.localization[self.name]['list_prefix']
            for date, shadow_message in shadow_list:
                if len(list_message) + len(shadow_message) < config.configuration['max_msg_length']:
                    list_message += shadow_message
        else:
            list_message = config.localization[self.name]['no_list']
        return {"response": list_message}

    @staticmethod
    def get_list_shadow(events, quantity):
        """
        Method to get a list of shadow events from multiple events, each sorted by date.
        :param events: A complete list of events.
        :param quantity: The amount of shadow events you want, up to a maximum set in settings.
        :return: A list of both events and shadow events, sorted by date.
        """
        list_with_shadow = []
        for event in events:
            event_tuple = (event.date, event.describe_short())
            list_with_shadow.append(event_tuple)
            shadow_events = event.get_shadow_events(quantity)
            for shadow_event in shadow_events:
                event_tuple = (shadow_event.date, shadow_event.describe_shadow())
                list_with_shadow.append(event_tuple)
        list_with_shadow = sorted(list_with_shadow)
        return list_with_shadow


class CreateEventCommand(Command):
    """
    Command class for Creating an event.
    """

    def __init__(self):
        super().__init__('create_event')
        self.description = self.description.format(config.configuration['sign'])
        self.parameters = self.parameters.format(config.configuration['calendar']['max_event_name'],
                                                 config.configuration['calendar']['max_event_description'])

    def in_call(self, command):
        if "event" in command and ("add" in command or "create" in command):
            return True
        return False

    def execute(self, param, message, system):
        if system.event_manager is None:
            raise CommandError("database_error", None)
        try:
            event_dict = event_parser.parse_event_string(param)
            event_dict["author"] = message.author.id
            logger.info("Attempting to create an event with the following parameters: {}".format(event_dict))

            if "channel" not in event_dict.keys() and message.guild:
                event_dict["channel"] = message.channel.name
            if "name" not in event_dict:
                raise event_parser.EventError("required_field_missing", "name")
            if "date" not in event_dict:
                raise event_parser.EventError("required_field_missing", "date")

            new_event = Event(**event_dict)

            event = system.event_manager.create_event(new_event)

            return {"response": config.localization[self.name]['prefix'].format(event.event_id),
                    "embed": event.get_event_embed(),
                    "add_id": message.author.id}
        except EventError as error:
            raise CommandError(error.message, error.parameters)


class EditEventCommand(Command):
    """
    Command class for Updating an event
    """

    def __init__(self):
        super().__init__('edit_event')
        self.parameters = self.parameters.format(config.configuration['sign'])

    def in_call(self, command):
        if "event" in command and ("edit" in command or "update" in command):
            return True
        return False

    def execute(self, param, message, system):
        if system.event_manager is None:
            raise CommandError("database_error", None)
        event_dict = event_parser.parse_event_string(param)
        id_str = event_dict.get("id", param.split(' ', 1)[0])
        try:
            event_id = int(id_str)
            event = system.event_manager.get_event(event_id)
            logger.info("Attempting to edit event {} with the following parameters: {}".format(event_id, event_dict))
            if event is None:
                raise CommandError("event_not_found", event_id)
            if event.author != message.author.id:
                raise CommandError("not_authorized", None)

            updated_event = system.event_manager.update_event(event_id, event_dict)
            return {"response": config.localization[self.name]['prefix'].format(event_id),
                    "embed": updated_event.get_event_embed(),
                    "add_id": message.author.id}
        except ValueError:
            raise CommandError("number_not_valid", id_str)
        except EventError as error:
            raise CommandError(error.message, error.parameters)


class DeleteEventCommand(Command):
    """
    Command class for Deleting an event.
    """

    def __init__(self):
        super().__init__('delete_event')

    def in_call(self, command):
        if "event" in command and "delete" in command:
            return True
        return False

    def execute(self, param, message, system):
        if system.event_manager is None:
            raise CommandError("database_error", None)
        try:
            event_id = int(param)
            logger.info("Attempting to delete event {}.".format(event_id))

            event = system.event_manager.get_event(event_id)
            if event is None:
                raise CommandError("event_not_found", event_id)
            if event.author != message.author.id:
                raise CommandError("not_authorized", None)
            event_name = event.name

            system.event_manager.delete_event(event_id)

            response = config.localization[self.name]['response'].format(event_id, event_name)
        except ValueError:
            raise CommandError("number_not_valid", param)
        return {"response": response}


class UnShadowCommand(Command):
    """
    Command class for allowing an event's shadow to be edited.
    """

    calendar_config = config.configuration['calendar']

    def __init__(self):
        super().__init__('unshadow_event')

    def in_call(self, command):
        if "shadow" in command:
            return True
        elif "reveal" in command and "event" in command:
            return True
        return False

    def execute(self, param, message, system):
        if system.event_manager is None:
            raise CommandError("database_error", None)
        parameter_match = re.search("(\\d+)-(\\d+)", param.replace(" ", ""))
        if parameter_match is None:
            raise CommandError("event_not_found", param)
        event_id = int(parameter_match[1])
        shadow_id = int(parameter_match[2])
        logger.info("Attempting to unshadow event {}-{}.".format(event_id, shadow_id))
        if 0 >= shadow_id or shadow_id >= self.calendar_config['max_shadows']:
            raise CommandError("invalid_shadow", param)

        event = system.event_manager.get_event(event_id)
        if event is None:
            raise CommandError("event_not_found", event_id)
        if event.author != message.author.id:
            raise CommandError("not_authorized", None)
        if not event.recur:
            raise CommandError("invalid_shadow", param)

        new_event_id = event_id
        for i in range(shadow_id+1):
            new_event = system.event_manager.pop_event(event_id)
            new_event_id = new_event.event_id

        return {"response": config.localization[self.name]['response'].format(param, new_event_id)}
