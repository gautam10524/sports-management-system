# Sports Management System (SportsMS)

A modern, responsive web application for managing sports teams, players, and match schedules. This project features a dual-role system for Administrators and Users, with dynamic data filtering and a premium glassmorphic UI.

## 🚀 Features

### For Admins
- **Full Management**: Create, Edit, and Delete teams, players, and matches.
- **Sport Filter**: Universal filter to manage multiple sports from a single dashboard.
- **Roster Control**: Enforce sport-specific roster limits and position constraints.
- **ID Access**: Toggleable database IDs for administrative tasks.

### For Users
- **Personal Dashboard**: View upcoming matches, team standings, and personal stats.
- **Browse Content**: Explore teams and player profiles with restricted editing rights.
- **Leaderboards**: Track rankings and champions across different sports.

---

## ⚙️ Setup Instructions

### 1. Backend Setup (The Engine)
The backend is built with Python and FastAPI. It handles all data storage and business logic.

1.  **Navigate to the Backend directory**:
    ```bash
    cd backend/backend
    ```
2.  **Create a Virtual Environment** (Optional but recommended):
    ```bash
    python -m venv venv
    ./venv/Scripts/activate  # On Windows
    source venv/bin/activate # On Mac/Linux
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Launch the API Server**:
    ```bash
    uvicorn app.main:app --reload
    ```
    *The server will start at `http://127.0.0.1:8000`.*

### 2. Frontend Setup (The Interface)
The frontend is a static application. It requires the backend to be running to fetch and display data.

1.  **Method A: Live Server (Recommended)**
    - If using VS Code, install the **Live Server** extension.
    - Right-click on `frontend/login.html` and select **"Open with Live Server"**.
2.  **Method B: Direct Browser**
    - Simply open `frontend/login.html` in any modern web browser (Edge, Chrome, Firefox).
3.  **Verify Connection**:
    - Ensure the URL in the browser bar is something like `http://127.0.0.1:5500/login.html` or the local file path.
    - The application will automatically communicate with the backend at `http://127.0.0.1:8000`.

---

## 🛠️ Technology Stack

- **Frontend**: Vanilla HTML5, CSS3, JavaScript.
    - **Styling**: Bootstrap 4.5 + Custom Glassmorphism UI.
    - **Animations**: AOS (Animate on Scroll).
- **Backend**: Python 3.9+ with **FastAPI**.
- **Database**: **SQLite3** (No separate installation required).

## 🌐 One-Link Deployment (Vercel.com)

Vercel is the fastest way to get a live, high-performance link for free.

### 1. Unified Structure
I have added a `vercel.json` file to the project. This tells Vercel how to host both your Python Backend and your Glassmorphic Frontend together.

### 2. Deployment Steps
1.  **Push to GitHub**: Ensure all latest changes are pushed to your GitHub repo.
2.  **Create Vercel Account**: Sign up at [Vercel.com](https://vercel.com) (use GitHub to login).
3.  **Import Project**:
    - Click **"Add New"** -> **"Project"**.
    - Connect your GitHub repository.
4.  **Configure Settings**:
    - **Framework Preset**: Other (it will detect Python automatically).
    - **Root Directory**: `backend/backend`
5.  **Deploy**: Click **"Deploy"**.

Once finished, Vercel will give you a link like `https://sports-ms.vercel.app`. Your site will load instantly every time!

---

## 🎨 Design Philosophy
The UI follows a **Glassmorphic** design language, using translucent cards with background blurs over high-quality sports imagery. It provides a premium, "living" feel with subtle hover animations and a professional dark-theme aesthetic.
