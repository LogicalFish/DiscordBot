import copy

from sqlalchemy.orm import make_transient

from database.models.event_model import Event


class EventManager:
    """
    Manager class for Creating, Reading, Updating, and Deleting calendar events.
    Uses the database for storing events.
    """

    def __init__(self, database_manager):
        self.database = database_manager
        self.altered = False

    def get_event(self, id_no):
        """
        Method for Reading a single event
        :param id_no: Integer: The ID number of the event.
        :return: -
        """
        event = self.database.fetch_one(Event, id_no)
        return event

    def get_all_events(self):
        """
        Method for reading ALL event entries
        :return: A list of dictionaries, each containing event data, sorted by date.
        """
        return self.database.select_all(Event)

    def create_event(self, event):
        """
        Method for Creating an event.
        :param event:
        :return: -
        """
        new_event = self.database.insert(event)
        self.altered = True
        return new_event

    def update_event(self, id_no, event_dict):
        """
        Method for Updating an event. Only allows the user that created the event to update it.
        :param id_no: Integer: The ID number of the event to be deleted.
        :param event_dict: A dictionary containing relevant event data.
        :return: The event dictionary of the event.
        """
        updated_event = self.database.update(Event, id_no, event_dict)
        if updated_event is not None:
            self.altered = True

        return updated_event

    def delete_event(self, id_no):
        """
        Method for Deleting an event. Only allows the user that created the event to delete it.
        :param id_no: Integer: The ID number of the event to be deleted.
        :return: The name of the deleted event.
        """
        deleted = self.database.delete(Event, id_no)
        if deleted:
            self.altered = True
        return deleted

    def pop_event(self, id_no):
        """
        Method for pushing back a recurring event after creating an exact copy.
        :param id_no: The integer of the event to recur.
        :return: The new event (an exact copy of the event)
        """
        session = self.database.Session()
        event = session.query(Event).filter(Event.event_id == id_no).first()
        if not event:
            session.close()
            return None
        new_event = copy.deepcopy(event)
        make_transient(new_event)
        new_event.recur = None
        new_event.event_id = None
        new_event = self.create_event(new_event)
        event.recur_self()
        session.commit()
        session.close()
        self.altered = True
        return new_event

    def recur_event(self, id_no):
        session = self.database.Session()
        event = session.query(Event).filter(Event.event_id == id_no).first()
        if not event:
            session.close()
            return None
        event.recur_self()
        session.commit()
        session.close()
        self.altered = True