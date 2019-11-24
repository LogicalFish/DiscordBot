from sqlalchemy import Column, String, BigInteger

from database import Base

from config import configuration

class Nickname(Base):
    __tablename__ = 'nicknames'

    user_id = Column('user_id', BigInteger, primary_key=True)
    nickname = Column('nickname', String(configuration['nicknames']['max_length']))

    def __init__(self, user_id, nickname):
        self.user_id = user_id
        self.nickname = nickname
