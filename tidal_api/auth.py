from pathlib import Path
from tidal_api.browser_session import BrowserSession

CONFIG_DIR = Path.home() / ".config" / "tidalapi"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

SESSION_FILE = CONFIG_DIR / "session.json"

session = BrowserSession()
session.login_session_file_auto(
    session_file=SESSION_FILE,
    do_pkce=True,
)
