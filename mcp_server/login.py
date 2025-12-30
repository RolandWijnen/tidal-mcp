import tidalapi
from pathlib import Path

SESSION_FILE = Path("/root/.config/tidalapi-session.json")

print("Starting TIDAL login...")

session = tidalapi.Session()
code = session.login_oauth_simple()

print(f"Visit {code.url} to log in. Code expires in {code.expires} seconds.")

input("Press Enter after completing login in browser...")

SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
session.save_session_to_file(SESSION_FILE)

print(f"Session saved to {SESSION_FILE}")
