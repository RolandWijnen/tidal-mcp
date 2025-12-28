import tidalapi

print("Starting TIDAL login...")

session = tidalapi.Session()
session.login_oauth_simple()

session.save_session_to_file("/root/.config/tidalapi-session.json")

print("Login successful. Session saved.")
