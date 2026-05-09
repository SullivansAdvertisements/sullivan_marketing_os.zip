def build_spotify_music_plan(inputs: dict) -> dict:
    genre = inputs.get("niche", "music")
    artist = inputs.get("name", "Artist")
    return {
        "Artist/Brand": artist,
        "Playlist Strategy": [
            "Pitch to genre-matched independent curators.",
            "Build a pre-save or fan-link landing page before promotion.",
            "Run short-form video ads to warm traffic before playlist outreach.",
            "Track every submission: curator, playlist, status, date, result."
        ],
        "Target Countries": ["United States", "Canada", "United Kingdom", "Australia", "Germany", "Netherlands", "Brazil", "Mexico", "South Africa", "Nigeria"],
        "Genre Keywords": [genre, f"{genre} playlist", f"new {genre}", f"{genre} music video", "independent artist"],
        "Fan Audiences": ["similar artists", "genre playlist listeners", "music video viewers", "Spotify/YouTube engagers"],
        "KPIs": ["streams", "saves", "followers", "playlist adds", "cost per listener", "listener retention"],
        "Templates": ["single release", "album rollout", "music video push", "playlist pitching sprint"],
    }
