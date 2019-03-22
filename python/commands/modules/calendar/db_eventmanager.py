from commands.modules.calendar.event_validator import clean_input


class EventManager:

    def __init__(self, db):
        self.db_manager = db
        self.table = 'events'
        self.primary_key = 'event_id'

    def create_event(self, user_input):
        var_dict = clean_input(user_input, self.db_manager)
        self.db_manager.insert(var_dict, self.table)

    def get_event(self, id_no):
        columns = self.db_manager.get_columns(self.table)
        row = self.db_manager.select_one(id_no, self.primary_key, self.table)
        if row is not None:
           return dict(zip(columns, row))
        else:
            return False

    def get_all_events(self):
        columns = self.db_manager.get_columns(self.table)
        rows = self.db_manager.get_rows(self.table)
        all_events = []
        for row in rows:
            event = dict(zip(columns, row))
            all_events.append(event)
        return all_events

    def delete_event(self, id_no):
        self.db_manager.delete(id_no, self.primary_key, self.table)

from database.db_manager import DatabaseManager


db_man = DatabaseManager()
e_man = EventManager(db_man)
userinput = 'name="Christmas Eve", description="Gift-giving time", date="December 24th", creator="me" time="18:00" borgle="bargle"'
e_man.create_event(userinput)
print("DB_MAN SELECT ONE:")
print(db_man.select_one(2, 'event_id', 'events'))
print("E_MAN GET ONE")
print(e_man.get_event(2))
ii = e_man.get_all_events()
print("E_MAN GET ALL")
for i in ii:
    print(i)
