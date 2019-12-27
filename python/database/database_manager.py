from sqlalchemy.orm import sessionmaker

from database.database_connection import DatabaseConnection


class DatabaseManager:
    """Manager for the database."""

    def __init__(self):
        self.db = DatabaseConnection()
        self.Session = sessionmaker(bind=self.db.engine)

    def insert(self, item):
        """
        Insert a new entry into a database.
        """
        session = self.Session()
        session.add(item)
        session.flush()
        session.expunge(item)
        session.commit()
        session.close()
        return item

    def update(self, table, pk_value, var_dict):
        """
        Update an entry in the database.
        """
        session = self.Session()
        item_to_update = session.query(table).filter(list(table.__table__.primary_key)[0] == pk_value).first()
        if item_to_update:
            if callable(getattr(item_to_update, "update", None)):
                item_to_update.update(**var_dict)
            else:
                for key, value in var_dict.items():
                    setattr(item_to_update, key, value)
            session.flush()
            session.expunge(item_to_update)
            session.commit()
        session.close()
        return item_to_update

    def delete(self, table, pk_value):
        """
        Delete an entry in the database.
        """
        session = self.Session()
        entry = session.query(table).filter(list(table.__table__.primary_key)[0] == pk_value).first()
        if entry:
            session.delete(entry)
            session.commit()
            result = True
        else:
            result = False
        session.close()
        return result

    def fetch_one(self, table, pk_value):
        """
        Read an entry in the database.
        """
        session = self.Session()
        result = session.query(table).filter(list(table.__table__.primary_key)[0] == pk_value).first()
        if result:
            session.expunge(result)
        session.close()
        return result

    def select_all(self, table):
        """
        Reads an entire table.
        """
        session = self.Session()
        results = session.query(table).all()
        session.expunge_all()
        session.close()
        return results

    def insert_bot(self, bot):
        from database.models import Birthday
        from database.models import Nickname
        from datetime import datetime

        session = self.Session()
        if not session.query(Birthday).filter(Birthday.user_id == bot.id).first():
            bot_birthday = datetime(2019, 2, 12, 12, 0, 0)
            session.add(Birthday(bot.id, bot_birthday))
        if not session.query(Nickname).filter(Nickname.user_id == bot.id).first():
            bot_nickname = "Project Game Master"
            session.add(Nickname(bot.id, bot_nickname))
        session.commit()
        session.close()
