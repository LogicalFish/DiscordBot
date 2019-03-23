from commands.modules.calendar.event_model import EventModel


class EventManager:

    def __init__(self, db):
        self.db_manager = db
        self.model = EventModel()

    def create_event(self, event_dict):
        self.model.validate_required_fields(event_dict)
        new_event_id = self.db_manager.insert(event_dict, self.model.TABLE_NAME)
        return self.get_event(new_event_id)

    def update_event(self, id_no, event_dict, user=None):
        event = self.get_event(id_no)
        if event:
            if user is None or event[self.model.author_key] == user:
                self.db_manager.update(event_dict, id_no, self.model.PRIMARY_KEY, self.model.TABLE_NAME)
                return self.get_event(id_no)
            else:
                raise ValueError("Jij bent niet de eigenaar van dit evenement.")
        else:
            raise ValueError("Geen event met ID '{}' gevonden".format(id_no))

    def get_event(self, id_no):
        columns = self.db_manager.get_columns(self.model.TABLE_NAME)
        row = self.db_manager.select_one(id_no, self.model.PRIMARY_KEY, self.model.TABLE_NAME)
        if row:
            return dict(zip(columns, row))
        else:
            return False

    def get_all_events(self):
        columns = self.db_manager.get_columns(self.model.TABLE_NAME)
        rows = self.db_manager.get_rows(self.model.TABLE_NAME, sort="date")
        all_events = []
        for row in rows:
            event = dict(zip(columns, row))
            all_events.append(event)
        return all_events

    def delete_event(self, id_no, user=None):
        event = self.get_event(id_no)
        if event:
            if user is None or event[self.model.author_key] == user:
                self.db_manager.delete(id_no, self.model.PRIMARY_KEY, self.model.TABLE_NAME)
                return "Event {}: {} deleted.".format(id_no, event["name"])
            else:
                return "[ERROR]: Jij bent niet de eigenaar van dit evenement."
        else:
            return "[ERROR]: Geen event met ID '{}' gevonden".format(id_no)
