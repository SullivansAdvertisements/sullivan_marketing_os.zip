def build_spotify_plan(artist, song, genre, budget, locations):
    return {
        "Playlist Pitching Strategy": [
            "Build a clean pitch with song mood, genre, story, comparable artists, and target listener profile.",
            "Prioritize independent curators, niche genre playlists, local market playlists, and user-generated playlists.",
            "Track every playlist name, contact, submission date, response, placement, and estimated audience."
        ],
        "Fan Targeting": [genre, "similar artist fans", "music video viewers", "playlist listeners", "concert/festival fans"],
        "Country Targets": locations or "United States, Canada, United Kingdom, Australia, Germany, Brazil, Mexico, Philippines, Nigeria, South Africa",
        "Estimated Streams": int(float(budget) / 0.04),
        "Estimated Saves": int(float(budget) / 0.04 * 0.06),
        "Estimated Followers": int(float(budget) / 0.04 * 0.018),
        "Templates": ["Single release sprint", "EP awareness plan", "Album rollout", "Music video view + streaming retargeting"]
    }