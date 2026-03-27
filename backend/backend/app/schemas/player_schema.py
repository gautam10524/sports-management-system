from pydantic import BaseModel
from typing import Optional

class PlayerCreate(BaseModel):
    name: str
    age: Optional[int] = 0
    position: str
    sport: Optional[str] = None
    team_id: Optional[str] = None
    history: Optional[str] = ""
    awards: Optional[str] = ""

class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    position: Optional[str] = None
    sport: Optional[str] = None
    team_id: Optional[str] = None
    history: Optional[str] = None
    awards: Optional[str] = None

class Player(BaseModel):
    id: str
    name: str
    age: Optional[int] = 0
    position: str
    sport: Optional[str] = None
    team_id: Optional[str] = None
    history: Optional[str] = ""
    awards: Optional[str] = ""

    class Config:
        from_attributes = True