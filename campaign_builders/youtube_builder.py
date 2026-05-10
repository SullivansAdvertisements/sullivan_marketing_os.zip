def build_youtube_campaign(brand, video_topic, goal, budget, audience):
    return {
        "Campaign Structure": ["Skippable in-stream", "YouTube Shorts", "In-feed video discovery", "Retargeting viewers"],
        "In-stream Hooks": [
            f"Stop scrolling if you care about {video_topic}.",
            f"{brand} just dropped something different.",
            "Most people miss this part. Watch this."
        ],
        "Shorts Hooks": ["This is your sign.", "You have 3 seconds.", "Nobody is saying this enough."],
        "Script Ideas": [
            "Problem → proof → offer → CTA",
            "Behind the scenes → transformation → CTA",
            "Fast hook → best moment → replay-worthy ending"
        ],
        "Targeting": [audience, "custom intent keywords", "similar channels", "topic targeting", "remarketing"],
        "Keyword Targeting": [video_topic, f"{video_topic} reaction", f"best {video_topic}", f"{video_topic} music video"],
        "Placement Ideas": ["similar artist channels", "review channels", "playlist channels", "niche education channels"],
        "CPV Estimate": "$0.02 - $0.08 depending on niche, geography, creative, and targeting.",
        "Optimization": ["Cut weak hooks", "Separate Shorts and in-stream", "Retarget 25%+ viewers", "Scale lowest CPV with strong watch time"]
    }