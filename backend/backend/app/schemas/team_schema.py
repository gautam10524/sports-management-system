from pydantic import BaseModel

class TeamCreate(BaseModel):
    name: str
    coach: str
    sport: str


class Team(BaseModel):
    id: str
    name: str
    coach: str
    sport: str

    class Config:
        from_attributes = True