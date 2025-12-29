import tidalapi
from pathlib import Path
import threading

_session = None
_lock = threading.Lock()

SESSION_FILE = Path("/root/.config/tidalapi-session.json")

def get_session() -> tidalapi.Session:
    global _session

    with _lock:
        if _session is None:
            session = tidalapi.Session()

            if not SESSION_FILE.exists():
                raise RuntimeError(
                    "TIDAL is not authenticated.\n"
                    "Run:\n"
                    "  docker compose run --rm tidal-mcp python mcp_server/login.py"
                )

            session.load_session_from_file(SESSION_FILE)

            if not session.user:
                raise RuntimeError("TIDAL session file exists but is invalid.")

            _session = session

        return _session
