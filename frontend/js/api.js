const API = "http://127.0.0.1:8000"

function getSportFilter() {
  const isAdmin = localStorage.getItem("is_admin") === "true";
  if (isAdmin) {
    return localStorage.getItem("admin_filter_sport") || "All";
  } else {
    return localStorage.getItem("user_sport") || "All";
  }
}

// Teams
async function getTeams() {
  const sport = getSportFilter();
  const res = await fetch(API + "/teams/?sport=" + sport);
  return res.json()
}

// Players
async function getPlayers() {
  const sport = getSportFilter();
  const res = await fetch(API + "/players/?sport=" + sport);
  return res.json()
}

// Matches
async function getMatches() {
  const sport = getSportFilter();
  const res = await fetch(API + "/matches/?sport=" + sport);
  return res.json()
}

// Leaderboard
async function getLeaderboard() {
  const sport = getSportFilter();
  const res = await fetch(API + "/teams/leaderboard?sport=" + sport);
  return res.json()
}

// Helper to check login status
function checkAuth(requireAdmin = false) {
  const userId = localStorage.getItem("user_id");
  const isAdmin = localStorage.getItem("is_admin") === "true";

  if (!userId) {
    window.location.href = "login.html";
    return;
  }

  if (requireAdmin && !isAdmin) {
    window.location.href = "user.html";
    return;
  }
}

function handleLogout() {
  localStorage.clear();
  window.location.href = "login.html";
}

document.addEventListener("DOMContentLoaded", () => {
  const userId = localStorage.getItem("user_id");
  const isAdmin = localStorage.getItem("is_admin") === "true";
  const userName = localStorage.getItem("user_name");
  const currentFilter = localStorage.getItem("admin_filter_sport") || "All";

  // Hide admin-only elements for non-admins
  if (!isAdmin) {
    const style = document.createElement('style');
    style.innerHTML = '.admin-only { display: none !important; }';
    document.head.appendChild(style);
  }

  // Global Back Button Injection
  const headerContainer = document.querySelector(".site-navbar .container .d-flex");
  if (headerContainer && !document.getElementById("globalBackBtn")) {
    const backDiv = document.createElement("div");
    backDiv.id = "globalBackBtn";
    backDiv.className = "mr-3";
    // We use history.back() for general back navigation
    backDiv.innerHTML = `
      <a href="javascript:history.back()" class="btn btn-sm btn-outline-light d-flex align-items-center" style="border-radius: 20px; padding: 5px 15px; border: 1px solid rgba(255,255,255,0.3); background: rgba(255,255,255,0.05); transition: all 0.3s;">
        <span class="icon-keyboard_backspace" style="margin-right: 5px;"></span>
        <span style="font-weight: 700;">Back</span>
      </a>
    `;
    headerContainer.prepend(backDiv);

    // Hover effect
    const btn = backDiv.querySelector('a');
    btn.onmouseover = () => { btn.style.background = "rgba(255,255,255,0.15)"; btn.style.borderColor = "rgba(255,255,255,0.5)"; };
    btn.onmouseout = () => { btn.style.background = "rgba(255,255,255,0.05)"; btn.style.borderColor = "rgba(255,255,255,0.3)"; };
  }

  if (userId) {
    const navUl = document.querySelector(".site-menu.main-menu");
    if (navUl) {
      // Create a wrapper li for our admin tools / greeting
      const li = document.createElement("li");
      li.style.cssText = "display: inline-flex; align-items: center; margin-left: 20px; gap: 10px;";

      // 1. Sport Filter (Admin Only)
      if (isAdmin) {
        const sports = ["All", "Football", "Basketball", "Cricket", "Soccer", "Badminton", "Tennis", "Rugby", "Volleyball"];
        const select = document.createElement("select");
        select.className = "form-control form-control-sm";
        select.style.cssText = "width: 120px; background: rgba(255,255,255,0.1); color: #white; border: 1px solid rgba(255,255,255,0.2); border-radius: 20px; cursor: pointer; color: white;";
        
        sports.forEach(s => {
          const opt = document.createElement("option");
          opt.value = s;
          opt.textContent = s;
          opt.style.backgroundColor = "#101622";
          if (s === currentFilter) opt.selected = true;
          select.appendChild(opt);
        });

        select.onchange = (e) => {
          localStorage.setItem("admin_filter_sport", e.target.value);
          window.location.reload();
        };

        const filterLabel = document.createElement("span");
        filterLabel.className = "text-white-50";
        filterLabel.style.fontSize = "0.8rem";
        filterLabel.textContent = "Sport:";
        
        li.appendChild(filterLabel);
        li.appendChild(select);
      }

      // 2. Greeting
      const greeting = isAdmin ? "Hi Admin!" : `Hi ${userName || "User"}!`;
      const span = document.createElement("span");
      span.className = "text-white font-weight-bold";
      span.style.whiteSpace = "nowrap";
      span.textContent = greeting;
      li.appendChild(span);

      // 3. Logout Button
      const btn = document.createElement("button");
      btn.className = "btn btn-primary btn-sm px-3 py-1";
      btn.style.borderRadius = "20px";
      btn.textContent = "Logout";
      btn.onclick = handleLogout;
      li.appendChild(btn);

      navUl.appendChild(li);
    }
  }
});