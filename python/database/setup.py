import settings as s
from commands.modules.calendar.event_model import EventModel
from database.db_connection import DatabaseConnection
from database.decorators import CursorDecorator

db = DatabaseConnection()
em = EventModel()
event_table = em.create_table_sql()

@CursorDecorator(db.conn)
def create_tables(commands, cur=None):
    for command in commands:
        cur.execute(command)
    db.conn.commit()


if __name__ == '__main__':
    create_tables([event_table])
    db.close_connection()
