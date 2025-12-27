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
            session.load_session_from_file(SESSION_FILE)

            if not session.check_login():
                raise RuntimeError(
                    "TIDAL session not authenticated. "
                    "Run `docker compose --profile auth run --rm tidal-auth` first."
                )

            _session = session

        return _session
