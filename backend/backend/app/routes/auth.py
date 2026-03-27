from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User
from app.models.player_model import Player
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Auth"])

class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    role: str = "player"  # admin or player
    sport: Optional[str] = None
    age: Optional[int] = None
    dob: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

def calculate_age(dob_str):
    if not dob_str:
        return 0
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d")
        today = datetime.now()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    except:
        return 0

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Calculate age from DOB if DOB is provided
    age = user.age
    if user.dob:
        age = calculate_age(user.dob)
    
    status = "pending"
    if user.role == "admin":
        status = "accepted"
    
    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
        role=user.role,
        sport=user.sport,
        age=age,
        dob=user.dob,
        status=status
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "id": new_user.id}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email, User.password == user.password).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if db_user.status == "rejected":
        # Requirement #3: Show that the admin has rejected you
        return JSONResponse(status_code=403, content={"detail": "The admin has rejected you.", "id": db_user.id})
    
    return {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email,
        "role": db_user.role,
        "sport": db_user.sport,
        "status": db_user.status,
        "is_admin": db_user.role == "admin"
    }

@router.get("/users/pending")
def get_pending_users(db: Session = Depends(get_db)):
    return db.query(User).filter(User.status == "pending", User.role == "player").all()

@router.post("/users/{user_id}/approve")
def approve_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.status = "accepted"
    
    # Create a Player record if not already exists
    player = db.query(Player).filter(Player.user_id == user_id).first()
    if not player:
        new_player = Player(
            name=db_user.name,
            age=db_user.age or 0,
            position="Player", # Default position
            sport=db_user.sport,
            user_id=db_user.id
        )
        db.add(new_player)
    
    db.commit()
    return {"message": "User approved and player record created"}

@router.post("/users/{user_id}/reject")
def reject_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.status = "rejected"
    db.commit()
    return {"message": "User rejected"}

@router.post("/users/{user_id}/reapply")
def reapply_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.status = "pending"
    db.commit()
    return {"message": "Reapplied successfully"}

@router.get("/users/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email,
        "role": db_user.role,
        "sport": db_user.sport,
        "age": db_user.age,
        "dob": db_user.dob,
        "status": db_user.status,
        "is_admin": db_user.role == "admin"
    }
