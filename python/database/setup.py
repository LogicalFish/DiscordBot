import settings as s
from database.db_connection import DatabaseConnection
from database.decorators import CursorDecorator

db = DatabaseConnection()
event_table = """
    CREATE TABLE events (
        event_id SERIAL PRIMARY KEY,
        name VARCHAR({}) NOT NULL,
        date TIMESTAMP NOT NULL,
        creator VARCHAR(255) NOT NULL,
        description VARCHAR({}),
        channel VARCHAR(255),
        tag VARCHAR(255),
        reminder VARCHAR(255),
        recur INTEGER
    )         
    """.format(s.MAX_EVENT_NAME, s.MAX_EVENT_DESCRIPTION)


@CursorDecorator(db.conn)
def create_tables(commands, cur=None):
    for command in commands:
        cur.execute(command)
    db.conn.commit()


if __name__ == '__main__':
    create_tables([event_table])
    db.close_connection()
