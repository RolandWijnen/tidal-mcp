from mcp.server.fastmcp import FastMCP
from typing import Optional, List
import tidalapi
import sys

print("TIDAL MCP starting...", file=sys.stderr)

mcp = FastMCP("TIDAL MCP")

# -------------------------------------------------------------------
# TIDAL SESSION (single source of truth)
# -------------------------------------------------------------------

def get_session() -> tidalapi.Session:
    """
    Loads an existing authenticated TIDAL session.
    Assumes tidal-auth has already completed PKCE login.
    """
    session = tidalapi.Session()
    logged_in = session.login_session()

    if not logged_in:
        raise RuntimeError(
            "Not authenticated with TIDAL. "
            "Run the tidal-auth container to login first."
        )

    return session


# Create session once at startup (hard fail if not logged in)
try:
    session = get_session()
    user = session.user
except Exception as e:
    print(f"[FATAL] {e}", file=sys.stderr)
    sys.exit(1)

# -------------------------------------------------------------------
# TOOLS
# -------------------------------------------------------------------

@mcp.tool()
def get_favorite_tracks(limit: int = 20) -> dict:
    """
    Retrieves the user's favorite tracks from TIDAL.
    """
    try:
        favorites = user.favorites.tracks(limit=limit)

        tracks = []
        for track in favorites:
            tracks.append({
                "id": track.id,
                "title": track.name,
                "artist": track.artist.name,
                "album": track.album.name,
                "duration": track.duration,
                "url": track.url
            })

        return {
            "status": "success",
            "tracks": tracks,
            "track_count": len(tracks)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@mcp.tool()
def get_user_playlists() -> dict:
    """
    Fetches the user's playlists.
    """
    try:
        playlists = user.playlists()

        result = []
        for pl in playlists:
            result.append({
                "id": pl.id,
                "title": pl.name,
                "description": pl.description,
                "track_count": pl.num_tracks,
                "url": f"https://tidal.com/playlist/{pl.id}",
                "last_updated": pl.last_updated
            })

        return {
            "status": "success",
            "playlists": result,
            "playlist_count": len(result)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@mcp.tool()
def get_playlist_tracks(playlist_id: str, limit: int = 100) -> dict:
    """
    Retrieves tracks from a playlist.
    """
    try:
        playlist = session.playlist(playlist_id)
        items = playlist.tracks(limit=limit)

        tracks = []
        for track in items:
            tracks.append({
                "id": track.id,
                "title": track.name,
                "artist": track.artist.name,
                "album": track.album.name,
                "duration": track.duration,
                "url": track.url
            })

        return {
            "status": "success",
            "playlist": {
                "id": playlist.id,
                "title": playlist.name,
                "description": playlist.description
            },
            "tracks": tracks,
            "track_count": len(tracks)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@mcp.tool()
def create_tidal_playlist(
    title: str,
    track_ids: List[str],
    description: str = ""
) -> dict:
    """
    Creates a new playlist and adds tracks to it.
    """
    try:
        playlist = user.create_playlist(title, description)
        playlist.add(track_ids)

        return {
            "status": "success",
            "playlist": {
                "id": playlist.id,
                "title": playlist.name,
                "url": f"https://tidal.com/playlist/{playlist.id}",
                "track_count": len(track_ids)
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
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
            "message": f"Playlist {playlist_id} deleted"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# -------------------------------------------------------------------
# MCP ENTRYPOINT
# -------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
