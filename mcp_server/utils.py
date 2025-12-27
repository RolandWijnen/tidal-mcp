import subprocess
import os
import pathlib
import shutil
import sys

# ------------------------------------------------------------------
# Path setup: ensure repo root is on PYTHONPATH
# ------------------------------------------------------------------
ROOT_DIR = pathlib.Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(ROOT_DIR))

# Define a configurable port with a default that's less likely to conflict
DEFAULT_PORT = 5050
FLASK_PORT = int(os.environ.get("TIDAL_FLASK_PORT", DEFAULT_PORT))

# Define the base URL for your Flask app using the configurable port
FLASK_APP_URL = f"http://127.0.0.1:{FLASK_PORT}"

# Define login URL (Docker host)
EXTERNAL_HOST = os.environ.get("TIDAL_EXTERNAL_HOST", "localhost")
FLASK_EXTERNAL_URL = f"http://{EXTERNAL_HOST}:{FLASK_PORT}"

# Define the path to the Flask app dynamically
CURRENT_DIR = pathlib.Path(__file__).parent.absolute()
FLASK_APP_PATH = os.path.join(CURRENT_DIR, "..", "tidal_api", "app.py")
FLASK_APP_PATH = os.path.normpath(FLASK_APP_PATH)  # Normalize the path

# Global variable to hold the Flask app process
flask_process = None

_flask_started = False
_flask_started_lock = threading.Lock()

def start_flask_app():
    print(f"Starting TIDAL Flask app...", file=sys.stderr)

    global _flask_started

    with _flask_started_lock:
        if _flask_started:
            return
        _flask_started = True

    from tidal_api.app import app  # import your Flask app object

    app.run(
        host="0.0.0.0",
        port=FLASK_PORT,
        debug=False,
        use_reloader=False
    )

    print(f"TIDAL Flask app exited", file=sys.stderr)

def shutdown_flask_app():
    """Shutdown the Flask app subprocess when the MCP server exits"""
    global flask_process
    
    if flask_process:
        print(f"Shutting down TIDAL Flask app...", file=sys.stderr)

        # Try to terminate gracefully first
        flask_process.terminate()
        try:
            # Wait up to 5 seconds for process to terminate
            flask_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # If it doesn't terminate in time, force kill it
            flask_process.kill()
        print(f"TIDAL Flask app shutdown complete", file=sys.stderr)


