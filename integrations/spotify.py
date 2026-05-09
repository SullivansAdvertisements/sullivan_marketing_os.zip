from __future__ import annotations
from utils.config import has_key

def spotify_status() -> dict:
    ready = has_key("SPOTIFY_CLIENT_ID") and has_key("SPOTIFY_CLIENT_SECRET")
    return {
        "ready": ready,
        "message": "Spotify credentials found." if ready else "Add SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET for live Spotify integration."
    }
