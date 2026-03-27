from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.models.match_model import Match
from app.models.team_model import Team
from app.schemas.match_schema import MatchCreate

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.post("/")
def create_match(match: MatchCreate, db: Session = Depends(get_db)):
    if match.team1_id == match.team2_id:
        raise HTTPException(status_code=400, detail="A team cannot play against itself.")

    team1 = db.query(Team).filter(Team.id == match.team1_id).first()
    team2 = db.query(Team).filter(Team.id == match.team2_id).first()

    if not team1 or not team2:
        raise HTTPException(status_code=404, detail="One or both teams not found.")

    if team1.sport.strip().lower() != team2.sport.strip().lower():
        raise HTTPException(status_code=400, detail="Teams must play the same sport.")

    # Check time overlap
    conflict = db.query(Match).filter(
        Match.match_date == match.match_date,
        ((Match.team1_id == match.team1_id) | (Match.team2_id == match.team1_id) |
         (Match.team1_id == match.team2_id) | (Match.team2_id == match.team2_id))
    ).first()

    if conflict:
        raise HTTPException(status_code=400, detail="One of the teams already has a match scheduled at this time.")

    new_match = Match(
        team1_id=match.team1_id,
        team2_id=match.team2_id,
        match_date=match.match_date,
        location=match.location
    )

    db.add(new_match)
    db.commit()
    db.refresh(new_match)

    return new_match


@router.get("/")
def get_matches(sport: str = "All", db: Session = Depends(get_db)):
    query = db.query(Match)
    if sport != "All":
        # Filter matches by sport via the teams
        target_teams = db.query(Team).filter(Team.sport.ilike(sport)).all()
        target_ids = [t.id for t in target_teams]
        query = query.filter(Match.team1_id.in_(target_ids))
    return query.all()


@router.get("/team/{team_id}")
def get_team_matches(team_id: str, db: Session = Depends(get_db)):
    matches = db.query(Match).filter(
        (Match.team1_id == team_id) | (Match.team2_id == team_id)
    ).all()
    return matches


@router.put("/{match_id}/result")
def update_match_result(match_id: str, score1: int, score2: int, db: Session = Depends(get_db)):

    match = db.query(Match).filter(Match.id == match_id).first()

    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    match.score_team1 = score1
    match.score_team2 = score2

    if score1 > score2:
        match.winner = match.team1_id
    elif score2 > score1:
        match.winner = match.team2_id
    else:
        match.winner = "Draw"

    db.commit()
    db.refresh(match)

    return match


@router.put("/{match_id}/abort")
def abort_match(match_id: str, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    match.winner = "Aborted"
    match.score_team1 = 0
    match.score_team2 = 0
    
    db.commit()
    db.refresh(match)
    return match


@router.delete("/{match_id}")
def delete_match(match_id: str, db: Session = Depends(get_db)):

    match = db.query(Match).filter(Match.id == match_id).first()

    if not match:
        return {"error": "Match not found"}

    db.delete(match)
    db.commit()

    return {"message": "Match deleted"}


@router.post("/generate-fixtures")
def generate_fixtures(db: Session = Depends(get_db)):
    teams = db.query(Team).all()

    if len(teams) < 2:
        return {"error": "Not enough teams to generate fixtures"}

    fixtures = []
    base_date = datetime.today().date()
    days_offset = 0

    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            t1 = teams[i]
            t2 = teams[j]
            
            if t1.sport.strip().lower() != t2.sport.strip().lower():
                continue

            match_date_str = str(base_date + timedelta(days=days_offset))
            
            # Simple check to avoid time overlap on the same day for these specific teams
            conflict = db.query(Match).filter(
                Match.match_date == match_date_str,
                ((Match.team1_id == t1.id) | (Match.team2_id == t1.id) |
                 (Match.team1_id == t2.id) | (Match.team2_id == t2.id))
            ).first()

            if conflict:
                days_offset += 1
                match_date_str = str(base_date + timedelta(days=days_offset))
            
            match = Match(
                team1_id=t1.id,
                team2_id=t2.id,
                match_date=match_date_str,
                location="Main Stadium"
            )

            db.add(match)
            db.commit()  # commit each to allow conflict checker to see it
            db.refresh(match)
            fixtures.append(match)
            days_offset += 1  # Space out matches

    return {
        "message": "Fixtures generated successfully",
        "total_matches": len(fixtures)
    }