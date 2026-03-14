from sqlalchemy import Column, String, Integer
import uuid
from app.database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)  # admin or player
    sport = Column(String, nullable=True)  # for players
    age = Column(Integer, nullable=True)
    dob = Column(String, nullable=True)