from modules.calendar.event_model import EventModel
from database.database_connection import DatabaseConnection
from database.decorators import CursorDecorator
from modules.nicknames import nickname_manager, nickname_config
from modules.birthday import birthday_manager
from bot_identity import identity_manager

db = DatabaseConnection()
em = EventModel()
event_table = em.create_table_sql()
ban_table = "{} ( {} BIGINT PRIMARY KEY );".format(identity_manager.BAN_TABLE,
                                                   identity_manager.PRIMARY_KEY)
name_table = "{} ( {} BIGINT PRIMARY KEY, {} VARCHAR({}) );".format(nickname_manager.NAME_TABLE,
                                                                    nickname_manager.PRIMARY_KEY,
                                                                    nickname_manager.SECONDARY,
                                                                    nickname_config.MAX_NICK_NAME)
birthday_table = "{} ( {} BIGINT PRIMARY KEY, {} TIMESTAMP );".format(birthday_manager.NAME_TABLE,
                                                                      birthday_manager.PRIMARY_KEY,
                                                                      birthday_manager.SECONDARY)


@CursorDecorator(db.conn)
def create_tables(commands, cur=None):
    for command in commands:
        cur.execute("CREATE TABLE IF NOT EXISTS {}".format(command))
    db.conn.commit()


if __name__ == '__main__':
    create_tables([event_table, ban_table, name_table, birthday_table])
    db.close_connection()
