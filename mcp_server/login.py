import tidalapi
from pathlib import Path

SESSION_FILE = Path("/root/.config/tidalapi-session.json")

print("Starting TIDAL login...")

session = tidalapi.Session()
session.login_oauth_simple()

SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
session.save_session_to_file(SESSION_FILE)

print("Login successful. Session saved.")
