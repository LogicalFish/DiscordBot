from datetime import timedelta

from modules.calendar.event_model import EventModel, EventError


class EventManager:
    """
    Manager class for Creating, Reading, Updating, and Deleting calendar events.
    Uses the database for storing events.
    """

    def __init__(self, database_manager):
        self.database = database_manager
        self.model = EventModel()
        self.altered = False

    def get_event(self, id_no):
        """
        Method for Reading a single event
        :param id_no: Integer: The ID number of the event.
        :return: A dictionary containing event data, or False if none could be found.
        """
        columns = self.database.get_columns(self.model.TABLE_NAME)
        row = self.database.select_one_row(id_no, self.model.PRIMARY_KEY, self.model.TABLE_NAME)
        if row:
            return dict(zip(columns, row))
        else:
            return False

    def get_all_events(self):
        """
        Method for reading ALL event entries
        :return: A list of dictionaries, each containing event data, sorted by date.
        """
        columns = self.database.get_columns(self.model.TABLE_NAME)
        rows = self.database.get_rows(self.model.TABLE_NAME, sort="date")
        all_events = []
        for row in rows:
            event = dict(zip(columns, row))
            all_events.append(event)
        return all_events

    def create_event(self, event_dict):
        """
        Method for Creating an event.
        :param event_dict: A dictionary containing relevant event data. Must contain all required fields.
        :return: The event dictionary of the event that has been created.
        """
        self.model.validate_required_fields(event_dict)
        new_event_id = self.database.insert(event_dict, self.model.TABLE_NAME, self.model.PRIMARY_KEY)
        self.altered = True
        return self.get_event(new_event_id)

    def update_event(self, id_no, event_dict, user=None):
        """
        Method for Updating an event. Only allows the user that created the event to update it.
        :param id_no: Integer: The ID number of the event to be deleted.
        :param event_dict: A dictionary containing relevant event data.
        :param user: The user trying to update the event. Should be None only if not called by a User.
        :return: The event dictionary of the event.
        """
        event = self.get_event(id_no)
        if event:
            if user is None or event[self.model.key_author] == user:
                self.database.update(event_dict, id_no, self.model.PRIMARY_KEY, self.model.TABLE_NAME)
                self.altered = True
                return self.get_event(id_no)
            else:
                raise EventError("not_authorized", None)
        else:
            raise EventError("event_not_found", id_no)

    def delete_event(self, id_no, user=None):
        """
        Method for Deleting an event. Only allows the user that created the event to delete it.
        :param id_no: Integer: The ID number of the event to be deleted.
        :param user: The user trying to update the event. Should be None only if not called by a User.
        :return: The name of the deleted event.
        """
        event = self.get_event(id_no)
        if event:
            if user is None or event[self.model.key_author] == user:
                self.database.delete(id_no, self.model.PRIMARY_KEY, self.model.TABLE_NAME)
                self.altered = True
                return event["name"]
            else:
                raise EventError("not_authorized", None)
        else:
            raise EventError("event_not_found", id_no)

    def event_recur(self, id_no):
        """
        Method for allowing an event to recur. If the event doesn't recur, nothing happens.
        :param id_no: Integer: The ID number of the event that should recur.
        """
        event = self.get_event(id_no)
        if event["recur"]:
            next_time = timedelta(days=event["recur"])
            new_date = event["date"] + next_time
            self.update_event(id_no, {"date": new_date})

    def pop_event(self, id_no, user=None):
        """
        Method for pushing back a recurring event after creating an exact copy.
        See shadow_events.py
        :param id_no: The integer of the event to recur.
        :param user: The user trying to create the new event. Should be None only if not called by a User.
        :return: The new event (an exact copy of the event)
        """
        event = self.get_event(id_no)
        if event:
            if user is None or event[self.model.key_author] == user:
                if event["recur"]:
                    event.pop("recur")
                    event.pop(self.model.PRIMARY_KEY)
                    new_event = self.create_event(event)
                    self.event_recur(id_no)
                    return new_event
                else:
                    raise EventError("invalid_shadow", id_no)
            else:
                raise EventError("not_authorized", None)
        else:
            raise EventError("event_not_found", id_no)
