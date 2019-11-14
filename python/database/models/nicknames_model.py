from sqlalchemy import Column, String, BigInteger

from database import Base
from modules.nicknames import nickname_config


class Nickname(Base):
    __tablename__ = 'nicknames'

    user_id = Column('user_id', BigInteger, primary_key=True)
    nickname = Column('nickname', String(nickname_config.MAX_NICK_NAME))

    def __init__(self, user_id, nickname):
        self.user_id = user_id
        self.nickname = nickname
