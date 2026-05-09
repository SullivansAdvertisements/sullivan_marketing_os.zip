def build_google_youtube_plan(inputs: dict, keywords: list[str] | None = None, creative: str = "") -> dict:
    keywords = keywords or []
    niche = inputs.get("niche", "campaign")
    return {
        "Google Search Structure": {
            "Campaigns": [f"{niche} - High Intent Search", f"{niche} - Competitor/Alternative Search"],
            "Ad Groups": keywords[:8] or ["brand keywords", "service keywords", "problem keywords", "buying intent keywords"],
            "Negative Keywords": ["free", "jobs", "scam", "download", "torrent", "cheap fake"],
            "Bidding": "Maximize clicks for testing, then Maximize conversions once tracking is clean.",
        },
        "YouTube Structure": {
            "Campaigns": ["Awareness video views", "Retargeting video viewers", "Conversion push"],
            "Hooks": [
                "Stop scrolling if you want better results from your next campaign.",
                "Here is the mistake most brands make before spending on ads.",
                "This is how we would launch this offer with a small budget."
            ],
            "Targeting": ["custom intent keywords", "in-market audiences", "remarketing", "similar channels/topics"],
        },
        "Creative": creative or "Generate scripts and hooks in Creative Studio.",
    }
