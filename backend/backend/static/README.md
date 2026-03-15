# League Mania - Sports Management System

A comprehensive sports management application to manage teams, players, matches, and leaderboards across various sports (Cricket, Football, Soccer, Basketball, etc.).

## 🏗 Project Structure
- **/backend**: FastAPI application with SQLite database.
- **/frontend**: Vanilla HTML/CSS/JS frontend (Bootstrap based).

---

## 🚀 Getting Started

### 1. Backend Setup (FastAPI)
The backend handles the data, sport-specific logic, and the AI assistant features.

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Server:**
   ```bash
   uvicorn app.main:app --reload
   ```
   *The API will be available at `http://127.0.0.1:8000`.*
   *Interactive Documentation: `http://127.0.0.1:8000/docs`*

### 2. Frontend Setup
The frontend is built with HTML5, CSS3, and JavaScript.

1. **Configure API URL:**
   Open the HTML files and ensure the `API` constant matches your backend URL:
   ```javascript
   const API = "http://127.0.0.1:8000";
   ```

2. **Open the App:**
   Simply open `login.html` in any modern browser. For the best experience (and to avoid CORS issues in some browsers), use a local server extension like "Live Server" in VS Code.

---

## 🛠 Features
- **Sport-Specific Match Scheduling**: Dynamic labels ("Team vs Team" or "Player vs Player") based on the sport.
- **Player History & Awards**: Detailed popups for player achievements.
- **Smart Leaderboards**: Individual leaderboards for each sport type.
- **Glassmorphism UI**: Modern, translucent design with `field.jpg` backgrounds.
- **AI Assistant**: Local AI suggestions for player training and position tips.
- **Team/Player ID Copy**: Circular sport icons for teams and clipboard shortcuts for easy management.

---

## 📦 Deployment Suggestions
- **Backend**: Deploy to **Render**, **Railway**, or **Heroku**.
- **Frontend**: Deploy to **Netlify**, **Vercel**, or **GitHub Pages**.

---

## 👥 Handover Checklist
- [ ] Transfer the GitHub repository.
- [ ] Share the `sports.db` file (if you want to keep current data).
- [ ] Ensure the Python version is 3.10+.
- [ ] Check CORS settings in `app/main.py`.
