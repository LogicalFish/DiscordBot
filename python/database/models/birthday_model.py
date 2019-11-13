from sqlalchemy import Column, DateTime, BigInteger

from database.database_connection import Base


class Birthday(Base):
    __tablename__ = 'birthdays'

    user_id = Column('user_id', BigInteger, primary_key=True)
    birthday = Column('birthday', DateTime)

    def __init__(self, user_id, birthday):
        self.user_id = user_id
        self.birthday = birthday
