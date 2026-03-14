from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import team_model, player_model, match_model, user_model
from app.routes import teams, players, matches, auth


Base.metadata.create_all(bind=engine)


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


@app.get("/")
def home():
    return {"message": "Sports Management System Backend Running"}


# AI Chat endpoint (mock - no API key needed)
@app.post("/ai/chat")
def ai_chat(request: dict):
    message = request.get("message", "")
    return {"reply": "AI Assistant: You said '" + message + "'. I am ready to help you with your sport details!"}