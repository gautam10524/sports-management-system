from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.team_model import Team
from app.models.player_model import Player
from app.models.match_model import Match
from app.schemas.team_schema import TeamCreate

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("/")
def create_team(team: TeamCreate, db: Session = Depends(get_db)):

    new_team = Team(
        name=team.name,
        coach=team.coach,
        sport=team.sport
    )

    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    return new_team


@router.get("/")
def get_teams(sport: str = "All", db: Session = Depends(get_db)):
    query = db.query(Team)
    if sport != "All":
        query = query.filter(Team.sport.ilike(sport))
    return query.all()


@router.get("/leaderboard")
def leaderboard(sport: str = "All", db: Session = Depends(get_db)):
    teams = db.query(Team)
    if sport != "All":
        teams = teams.filter(Team.sport.ilike(sport))
    teams = teams.all()

    # Get matches for all target teams
    team_ids = [t.id for t in teams]
    matches = db.query(Match).filter(
        (Match.team1_id.in_(team_ids)) | (Match.team2_id.in_(team_ids))
    ).all()

    # Initialize stats for all teams
    stats = {
        t.id: {"team_id": t.id, "team_name": t.name, "wins": 0, "draws": 0, "losses": 0, "points": 0}
        for t in teams
    }

    # Calculate stats based on matches
    for match in matches:
        # Check if the match actually has a recorded result/winner
        if match.winner is not None:
            if match.winner == "Draw":
                if match.team1_id in stats:
                    stats[match.team1_id]["draws"] += 1
                    stats[match.team1_id]["points"] += 1
                if match.team2_id in stats:
                    stats[match.team2_id]["draws"] += 1
                    stats[match.team2_id]["points"] += 1
            else:
                # Someone won
                winner_id = match.winner
                loser_id = match.team1_id if match.winner == match.team2_id else match.team2_id
                
                if winner_id in stats:
                    stats[winner_id]["wins"] += 1
                    stats[winner_id]["points"] += 3
                if loser_id in stats:
                    stats[loser_id]["losses"] += 1

    leaderboard = list(stats.values())
    leaderboard.sort(key=lambda x: x["points"], reverse=True)

    return leaderboard


@router.get("/dashboard")
def dashboard(sport: str = "All", db: Session = Depends(get_db)):

    team_q = db.query(Team)
    player_q = db.query(Player)
    match_q = db.query(Match)

    if sport != "All":
        team_q = team_q.filter(Team.sport.ilike(sport))
        # For players, we need to join with Team
        player_q = player_q.join(Team).filter(Team.sport.ilike(sport))
        # For matches, we need to join with Team (assuming team1 represents the sport)
        match_q = match_q.join(Team, Match.team1_id == Team.id).filter(Team.sport.ilike(sport))

    total_teams = team_q.count()
    total_players = player_q.count()
    total_matches = match_q.count()

    matches = match_q.all()

    points = {}

    for match in matches:

        if match.winner and match.winner != "Draw":

            if match.winner not in points:
                points[match.winner] = 0

            points[match.winner] += 3

    top_team_name = None
    top_points = 0

    if points:

        top_team_id = max(points, key=points.get)
        top_points = points[top_team_id]

        team = db.query(Team).filter(Team.id == top_team_id).first()

        if team:
            top_team_name = team.name

    recent_matches = db.query(Match).order_by(Match.match_date.desc()).limit(5).all()

    return {
        "total_teams": total_teams,
        "total_players": total_players,
        "total_matches": total_matches,
        "top_team": top_team_name,
        "top_points": top_points,
        "recent_matches": recent_matches
    }


@router.put("/{team_id}")
def update_team(team_id: str, team: TeamCreate, db: Session = Depends(get_db)):

    existing_team = db.query(Team).filter(Team.id == team_id).first()

    if not existing_team:
        return {"error": "Team not found"}

    existing_team.name = team.name
    existing_team.coach = team.coach
    existing_team.sport = team.sport

    db.commit()
    db.refresh(existing_team)

    return existing_team


@router.delete("/{team_id}")
def delete_team(team_id: str, db: Session = Depends(get_db)):

    team = db.query(Team).filter(Team.id == team_id).first()

    if not team:
        return {"error": "Team not found"}

    db.delete(team)
    db.commit()

    return {"message": "Team deleted successfully"}


@router.get("/{team_id}/details")
def team_details(team_id: str, db: Session = Depends(get_db)):

    team = db.query(Team).filter(Team.id == team_id).first()

    if not team:
        return {"error": "Team not found"}

    players = db.query(Player).filter(Player.team_id == team_id).all()

    matches = db.query(Match).filter(
        (Match.team1_id == team_id) | (Match.team2_id == team_id)
    ).all()

    matches_played = len(matches)

    matches_won = 0
    points = 0

    for m in matches:
        if m.winner == team_id:
            matches_won += 1
            points += 3

    return {
        "team_id": team.id,
        "team_name": team.name,
        "coach": team.coach,
        "sport": team.sport,
        "players": players,
        "matches_played": matches_played,
        "matches_won": matches_won,
        "points": points
    }