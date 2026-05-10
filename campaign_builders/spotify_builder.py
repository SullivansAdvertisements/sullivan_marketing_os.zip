def build_spotify_plan(inputs: dict) -> dict:
    genre = inputs.get("niche", "music")
    return {
        "Playlist Pitching Strategy": [
            "Pitch genre-matched independent curators.",
            "Use a fan-link landing page before pushing paid traffic.",
            "Retarget video viewers and engaged listeners.",
            "Track submissions by curator, playlist, date, status, and result.",
        ],
        "Recommended Countries": ["United States", "Canada", "United Kingdom", "Australia", "Germany", "Netherlands", "Brazil", "Mexico", "Nigeria", "South Africa"],
        "Genre Keywords": [genre, f"{genre} playlist", f"new {genre}", f"{genre} music video"],
        "Fan Audiences": ["similar artists", "Spotify listeners", "YouTube video viewers", "IG music fans"],
        "KPIs": ["streams", "saves", "followers", "playlist adds", "cost per listener"],
    }
