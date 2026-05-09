from __future__ import annotations
from utils.config import has_key

def youtube_status() -> dict:
    return {
        "ready": has_key("YOUTUBE_API_KEY"),
        "message": "YouTube API key found." if has_key("YOUTUBE_API_KEY") else "Add YOUTUBE_API_KEY for live YouTube data."
    }
