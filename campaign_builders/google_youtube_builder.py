def build_google_youtube_plan(inputs: dict, keywords=None, creative: str = "") -> dict:
    keywords = keywords or ["brand intent", "buying intent", "problem keywords", "competitor terms"]
    return {
        "Google Search Campaign": {
            "Ad Groups": keywords[:12],
            "Negative Keywords": ["free", "jobs", "scam", "torrent", "fake", "cheap"],
            "Bidding": "Maximize clicks for testing, then Maximize conversions after tracking is proven.",
        },
        "YouTube Campaign": {
            "Structure": ["Cold video views", "Warm retargeting", "Conversion push"],
            "Hooks": [
                "This is the campaign mistake most brands make.",
                "Here is how to launch smarter with your budget.",
                "Stop wasting ad spend before you test this angle."
            ],
            "Targeting": ["custom intent keywords", "similar channels", "in-market audiences", "remarketing"],
        },
        "Creative": creative or "Generate video hooks and scripts in Creative Studio.",
    }
