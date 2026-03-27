from sqlalchemy import Column, String, Integer, ForeignKey
import uuid
from app.database import Base

class Player(Base):

    __tablename__ = "players"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    position = Column(String, nullable=False)
    sport = Column(String, nullable=True)
    history = Column(String, default="")
    awards = Column(String, default="")

    team_id = Column(String, ForeignKey("teams.id"))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)