# Sports Management System (SportsMS)

A modern, responsive web application for managing sports teams, players, and match schedules. This project features a dual-role system for Administrators and Users, with dynamic data filtering and a premium glassmorphic UI.

## 🚀 Features

### For Admins
- **Full Management**: Create, Edit, and Delete teams, players, and matches.
- **Sport Filter**: Universal filter to manage multiple sports (Football, Basketball, Cricket, etc.) from a single dashboard.
- **Roster Control**: Enforce sport-specific roster limits and position constraints.
- **ID Access**: Quickly copy Team and Player IDs for administrative tasks.

### For Users
- **Personal Dashboard**: View upcoming matches, team standings, and personal stats.
- **Browse Content**: View all teams and player profiles across the platform.
- **Leaderboards**: Track rankings and champions across different sports.
- **Privacy**: Simplified view without complex IDs or administrative controls.

## 🛠️ Technology Stack

- **Frontend**: Vanilla HTML5, CSS3, JavaScript.
    - **Styling**: Bootstrap 4.5, Custom Glassmorphism UI, AOS (Animate on Scroll).
    - **Logic**: Async/Await Fetch API, LocalStorage session management.
- **Backend**: Python FastAPI.
    - **Database**: SQLite3.
    - **Architecture**: RESTful API design.

## 📁 Project Structure

```text
soccer-master/
├── frontend/             # HTML/JS/CSS source files
│   ├── js/api.js         # Core API utility and UI injection
│   ├── images/           # Assets (field.jpg, bg_3.jpg, etc.)
│   └── *.html            # Page templates
├── backend/
│   └── backend/          # FastAPI Implementation
│       ├── app/          # API routes and database models
│       ├── sports.db     # SQLite database
│       └── requirements.txt
└── .gitignore            # Git exclusion rules
```

## ⚙️ Setup Instructions

### Backend
1. Navigate to `backend/backend`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the server: `uvicorn app.main:app --reload`.

### Frontend
1. The frontend is static. Open `login.html` in any modern web browser or use a Live Server.
2. Ensure the backend is running at `http://127.0.0.1:8000`.

## 🎨 Design Philosophy
The UI follows a **Glassmorphic** design language, using translucent cards with background blurs over high-quality sports imagery (`field.jpg`). It provides a premium, "living" feel with subtle hover animations and a dark-theme aesthetic.
