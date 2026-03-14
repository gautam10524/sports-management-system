from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User
from pydantic import BaseModel
from typing import Optional

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

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
        role=user.role,
        sport=user.sport,
        age=user.age,
        dob=user.dob
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
    
    return {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email,
        "role": db_user.role,
        "sport": db_user.sport,
        "is_admin": db_user.role == "admin"
    }

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
        "is_admin": db_user.role == "admin"
    }
