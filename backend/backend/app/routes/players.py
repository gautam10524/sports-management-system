from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models.player_model import Player
from app.models.team_model import Team
from app.schemas.player_schema import PlayerCreate, PlayerUpdate

router = APIRouter(prefix="/players", tags=["Players"])

SPORT_RULES = {
    "football": 11,
    "soccer": 11,
    "cricket": 11,
    "basketball": 5,
    "volleyball": 6,
    "rugby": 15,
    "badminton": 2,
    "tennis": 2,
}

def check_team_capacity(db: Session, team_id: str, exclude_player_id: str = None):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    sport = (team.sport or "").strip().lower()
    max_players = SPORT_RULES.get(sport, 11)
    
    query = db.query(Player).filter(Player.team_id == team_id)
    if exclude_player_id:
        query = query.filter(Player.id != exclude_player_id)
        
    count = query.count()
    if count >= max_players:
        raise HTTPException(status_code=400, detail=f"Team roster is full for this sport (max {max_players})")


@router.post("/")
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    if player.team_id:
        team = db.query(Team).filter(Team.id == player.team_id).first()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        if player.sport and team.sport and player.sport.lower() != team.sport.lower():
            raise HTTPException(status_code=400, detail=f"Cannot add {player.sport} player to {team.sport} team")
        check_team_capacity(db, player.team_id)

    new_player = Player(
        name=player.name,
        age=player.age,
        position=player.position,
        sport=player.sport,
        team_id=player.team_id,
        history=player.history,
        awards=player.awards
    )

    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    return new_player


@router.get("/")
def get_players(sport: str = "All", db: Session = Depends(get_db)):
    query = db.query(Player)
    if sport != "All":
        # Check both player.sport and team.sport (for players already in teams)
        query = query.outerjoin(Team).filter(
            or_(
                Player.sport.ilike(sport),
                Team.sport.ilike(sport)
            )
        )
    return query.all()


@router.get("/team/{team_id}")
def get_players_by_team(team_id: str, db: Session = Depends(get_db)):
    players = db.query(Player).filter(Player.team_id == team_id).all()
    return players


@router.put("/{player_id}")
def update_player(player_id: str, player: PlayerUpdate, db: Session = Depends(get_db)):
    existing_player = db.query(Player).filter(Player.id == player_id).first()

    if not existing_player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Only update fields that were actually provided in the request
    update_data = player.model_dump(exclude_unset=True)
    
    # Check team capacity and sport match if team_id is being changed
    new_team_id = update_data.get("team_id")
    current_sport = update_data.get("sport") or existing_player.sport
    
    if new_team_id is not None and new_team_id != "" and new_team_id != existing_player.team_id:
        if existing_player.team_id:
             raise HTTPException(status_code=400, detail="Player is already assigned to another team. Remove them first.")
        
        team = db.query(Team).filter(Team.id == new_team_id).first()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        if current_sport and team.sport and current_sport.lower() != team.sport.lower():
            raise HTTPException(status_code=400, detail=f"Cannot add {current_sport} player to {team.sport} team")
        check_team_capacity(db, new_team_id, exclude_player_id=player_id)
    elif new_team_id == existing_player.team_id and update_data.get("sport"):
        # Even if team isn't changing, if sport is changing, we must check compatibility
        team = db.query(Team).filter(Team.id == existing_player.team_id).first()
        if team and update_data["sport"] and team.sport and update_data["sport"].lower() != team.sport.lower():
            raise HTTPException(status_code=400, detail=f"Cannot change sport to {update_data['sport']} while in a {team.sport} team")
    
    for field, value in update_data.items():
        setattr(existing_player, field, value)

    db.commit()
    db.refresh(existing_player)

    return existing_player


@router.get("/{player_id}")
def get_player(player_id: str, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.delete("/{player_id}")
def delete_player(player_id: str, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()

    if not player:
        return {"error": "Player not found"}

    db.delete(player)
    db.commit()

    return {"message": "Player deleted"}