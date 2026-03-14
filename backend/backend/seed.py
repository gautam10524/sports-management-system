"""
Seed script to create default admin user.
Run this once after starting the backend to create the admin account.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models.user_model import User
from app.models.team_model import Team
from app.models.player_model import Player
from app.models.match_model import Match

# Create all tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Create default admin user if not exists
admin = db.query(User).filter(User.email == "root@gmail.com").first()
if not admin:
    admin = User(
        name="Admin",
        email="root@gmail.com",
        password="root",
        role="admin",
        sport="All"
    )
    db.add(admin)
    db.commit()
    print("✅ Default admin user created (root@gmail.com / root)")
else:
    print("ℹ️  Admin user already exists")

db.close()
print("🎉 Database seeded successfully!")
