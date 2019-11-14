from sqlalchemy import Column, BigInteger, Integer

from database import Base

class Highscore(Base):
    __tablename__ = 'high_scores'

    user_id = Column('user_id', BigInteger, primary_key=True)
    score = Column('wheel_score', Integer)

    def __init__(self, user_id, score):
        self.user_id = user_id
        self.score = score
