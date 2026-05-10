def build_meta_plan(inputs: dict, creative: str = "") -> dict:
    return {
        "Objective": inputs.get("goal", "traffic").title(),
        "Ad Set Structure": [
            "Core cold audience: interests, behaviors, demographics",
            "Warm retargeting: engagers, website visitors, video viewers",
            "Lookalike audience once clean data is available",
        ],
        "Placements": ["Instagram Reels", "Instagram Stories", "Facebook Feed", "Instagram Feed"],
        "Optimization": "Start broad enough to learn, then cut weak ad sets after 48–72 hours.",
        "Creative": creative or "Generate ad copy in Creative Studio.",
        "KPIs": ["CTR", "CPC", "CPM", "CPA", "Conversion rate", "Engagement rate"],
    }
