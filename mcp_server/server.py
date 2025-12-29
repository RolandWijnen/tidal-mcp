from mcp.server.fastmcp import FastMCP
from typing import List
import sys

from mcp_server.tidal_session import get_session

print("TIDAL MCP starting...", file=sys.stderr)

mcp = FastMCP("TIDAL MCP")

# -------------------------------------------------------------------
# Load authenticated TIDAL session (single source of truth)
# -------------------------------------------------------------------

try:
    session = get_session()
    user = session.user
except Exception as e:
    print(f"[FATAL] {e}", file=sys.stderr)
    sys.exit(1)

# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------

def track_to_dict(track) -> dict:
    """Convert a tidalapi Track object to a safe serializable dict."""
    return {
        "id": track.id,
        "title": track.name,
        "artist": track.artist.name if track.artist else None,
        "album": track.album.name if track.album else None,
        "duration": track.duration,
        "explicit": track.explicit,
        "audio_quality": track.audio_quality,
        "url": f"https://tidal.com/browse/track/{track.id}",
    }


def playlist_to_dict(playlist) -> dict:
    """Convert a tidalapi Playlist object to a safe serializable dict."""
    return {
        "id": playlist.id,
        "title": playlist.name,
        "description": playlist.description,
        "track_count": playlist.num_tracks,
        "last_updated": playlist.last_updated,
        "url": f"https://tidal.com/browse/playlist/{playlist.id}",
    }

# -------------------------------------------------------------------
# TOOLS
# -------------------------------------------------------------------

@mcp.tool()
def get_favorite_tracks(limit: int = 20) -> dict:
    """
    Retrieves the user's favorite tracks from TIDAL.
    """
    try:
        limit = max(1, min(limit, 100))  # basic sanity clamp
        favorites = user.favorites.tracks(limit=limit)

        tracks = [track_to_dict(track) for track in favorites]

        return {
            "status": "success",
            "tracks": tracks,
            "track_count": len(tracks),
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
def get_user_playlists() -> dict:
    """
    Fetches the user's playlists.
    """
    try:
        playlists = user.playlists()

        result = [playlist_to_dict(pl) for pl in playlists]

        return {
            "status": "success",
            "playlists": result,
            "playlist_count": len(result),
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
def get_playlist_tracks(playlist_id: str, limit: int = 100) -> dict:
    """
    Retrieves tracks from a playlist.
    """
    try:
        limit = max(1, min(limit, 500))

        playlist = session.playlist(playlist_id)
        items = playlist.tracks(limit=limit)

        tracks = [track_to_dict(track) for track in items]

        return {
            "status": "success",
            "playlist": playlist_to_dict(playlist),
            "tracks": tracks,
            "track_count": len(tracks),
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
def create_tidal_playlist(
    title: str,
    track_ids: List[str],
    description: str = "",
) -> dict:
    """
    Creates a new playlist and adds tracks to it.
    """
    try:
        if not track_ids:
            return {
                "status": "error",
                "message": "track_ids must not be empty",
            }

        playlist = user.create_playlist(title, description)
        playlist.add(track_ids)

        return {
            "status": "success",
            "playlist": {
                "id": playlist.id,
                "title": playlist.name,
                "track_count": len(track_ids),
                "url": f"https://tidal.com/browse/playlist/{playlist.id}",
            },
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
def delete_tidal_playlist(playlist_id: str) -> dict:
    """
    Deletes a playlist.
    """
    try:
        playlist = session.playlist(playlist_id)
        playlist.delete()

        return {
            "status": "success",
            "message": f"Playlist {playlist_id} deleted",
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }

# -------------------------------------------------------------------
# MCP ENTRYPOINT
# -------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
