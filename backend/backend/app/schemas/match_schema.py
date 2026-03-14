from pydantic import BaseModel

class MatchCreate(BaseModel):
    team1_id: str
    team2_id: str
    match_date: str
    location: str


class Match(BaseModel):
    id: str
    team1_id: str
    team2_id: str
    match_date: str
    location: str
    score_team1: int = 0
    score_team2: int = 0
    winner: str = None
    
    class Config:
        from_attributes = True