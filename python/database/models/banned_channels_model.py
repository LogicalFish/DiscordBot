from sqlalchemy import Column, BigInteger

from database.database_connection import Base


class BannedChannel(Base):
    __tablename__ = 'banned_channels'

    channel_id = Column('channel_id', BigInteger, primary_key=True)

    def __init__(self, channel_id):
        self.channel_id = channel_id
