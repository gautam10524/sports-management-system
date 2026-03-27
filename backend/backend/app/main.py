from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .models import team_model, player_model, match_model, user_model
from .routes import teams, players, matches, auth
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from sqlalchemy import text

# Create tables
Base.metadata.create_all(bind=engine)

# Auto-migration for missing columns
def apply_migrations():
    with engine.connect() as conn:
        try:
            # Check for captain_id column in teams
            conn.execute(text("ALTER TABLE teams ADD COLUMN IF NOT EXISTS captain_id VARCHAR;"))
            
            # Check for columns in users table
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS status VARCHAR DEFAULT 'pending';"))
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS dob VARCHAR;"))
            
            # Check for columns in players table
            conn.execute(text("ALTER TABLE players ADD COLUMN IF NOT EXISTS sport VARCHAR;"))
            conn.execute(text("ALTER TABLE players ADD COLUMN IF NOT EXISTS user_id VARCHAR;"))

            # Check for columns in matches table
            conn.execute(text("ALTER TABLE matches ADD COLUMN IF NOT EXISTS mode VARCHAR DEFAULT 'Doubles';"))
            
            conn.commit()
            print("Migration: columns verified/added.")
        except Exception as e:
            print(f"Migration error: {e}")

apply_migrations()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(teams.router)
app.include_router(players.router)
app.include_router(matches.router)
app.include_router(auth.router)

# Use absolute paths for Vercel
current_dir = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(current_dir, "..", "static")

@app.get("/")
def home():
    login_file = os.path.join(static_path, "login.html")
    if os.path.exists(login_file):
        return FileResponse(login_file)
    return {"message": "Sports Management System Backend Running", "static_path": static_path}

# AI Chat endpoint
@app.post("/ai/chat")
def ai_chat(request: dict):
    message = request.get("message", "")
    return {"reply": "AI Assistant: You said '" + message + "'. I am ready to help you with your sport details!"}

# Mount static files (at the end)
if os.path.exists(static_path):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")