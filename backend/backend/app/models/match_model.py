from sqlalchemy import Column, String, Integer
import uuid
from app.database import Base

class Match(Base):

    __tablename__ = "matches"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    team1_id = Column(String, nullable=False)
    team2_id = Column(String, nullable=False)

    match_date = Column(String)
    location = Column(String)

    score_team1 = Column(Integer, default=0)
    score_team2 = Column(Integer, default=0)

    winner = Column(String)