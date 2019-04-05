import settings
from commands.modules.calendar.event_model import EventModel
from database.database_connection import DatabaseConnection
from database.decorators import CursorDecorator
from commands.modules.nicknames import nickname_manager
from responder import identity_manager

db = DatabaseConnection()
em = EventModel()
event_table = em.create_table_sql()
ban_table = "{} ( {} VARCHAR(255) PRIMARY KEY );".format(identity_manager.BAN_TABLE,
                                                         identity_manager.PRIMARY_KEY)
name_table = "{} ( {} VARCHAR(255) PRIMARY KEY, {} VARCHAR({}) );".format(nickname_manager.NAME_TABLE,
                                                                          nickname_manager.PRIMARY_KEY,
                                                                          nickname_manager.SECONDARY,
                                                                          settings.MAX_NICK_NAME)


@CursorDecorator(db.conn)
def create_tables(commands, cur=None):
    for command in commands:
        cur.execute("CREATE TABLE IF NOT EXISTS {}".format(command))
    db.conn.commit()


if __name__ == '__main__':
    create_tables([event_table, ban_table, name_table])
    db.close_connection()
