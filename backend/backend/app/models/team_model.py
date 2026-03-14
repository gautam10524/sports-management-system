from sqlalchemy import Column, String
import uuid
from app.database import Base

class Team(Base):

    __tablename__ = "teams"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    coach = Column(String, nullable=False)
    sport = Column(String, nullable=False)