import tidalapi
from pathlib import Path

SESSION_FILE = Path("/root/.config/tidalapi-session.json")

print("Starting TIDAL login...")

session = tidalapi.Session()

# This will start the PKCE flow
# 'login_oauth_simple' may return None if PKCE is disabled; instead use 'login_oauth'
code_url = session.login_oauth()
if not code_url:
    raise RuntimeError("Failed to start TIDAL PKCE login. Make sure PKCE is supported.")

print(f"Visit this URL in your browser: {code_url}")
input("Press Enter after completing login...")

# Save authenticated session
session.save_session_to_file(SESSION_FILE)
print(f"Session saved to {SESSION_FILE}")
