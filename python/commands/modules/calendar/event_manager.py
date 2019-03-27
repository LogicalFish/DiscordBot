from commands.modules.calendar.event_model import EventModel, EventError


class EventManager:

    def __init__(self, database_manager):
        self.database = database_manager
        self.model = EventModel()
        self.altered = False

    def get_event(self, id_no):
        columns = self.database.get_columns(self.model.TABLE_NAME)
        row = self.database.select_one(id_no, self.model.PRIMARY_KEY, self.model.TABLE_NAME)
        if row:
            return dict(zip(columns, row))
        else:
            return False

    def get_all_events(self):
        columns = self.database.get_columns(self.model.TABLE_NAME)
        rows = self.database.get_rows(self.model.TABLE_NAME, sort="date")
        all_events = []
        for row in rows:
            event = dict(zip(columns, row))
            all_events.append(event)
        return all_events

    def create_event(self, event_dict):
        self.model.validate_required_fields(event_dict)
        new_event_id = self.database.insert(event_dict, self.model.TABLE_NAME)
        self.altered = True
        return self.get_event(new_event_id)

    def update_event(self, id_no, event_dict, user=None):
        event = self.get_event(id_no)
        if event:
            if user is None or event[self.model.key_author] == user:
                self.database.update(event_dict, id_no, self.model.PRIMARY_KEY, self.model.TABLE_NAME)
                self.altered = True
                return self.get_event(id_no)
            else:
                raise EventError("Jij bent niet de eigenaar van dit evenement.")
        else:
            raise EventError("Geen event met ID '{}' gevonden".format(id_no))

    def delete_event(self, id_no, user=None):
        event = self.get_event(id_no)
        if event:
            if user is None or event[self.model.key_author] == user:
                self.database.delete(id_no, self.model.PRIMARY_KEY, self.model.TABLE_NAME)
                self.altered = True
                return "Event {}: {} deleted.".format(id_no, event["name"])
            else:
                raise EventError("[ERROR]: Jij bent niet de eigenaar van dit evenement.")
        else:
            raise EventError("[ERROR]: Geen event met ID '{}' gevonden".format(id_no))
