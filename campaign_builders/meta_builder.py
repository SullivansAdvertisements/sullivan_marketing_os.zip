def build_meta_plan(inputs: dict, creative: str = "") -> dict:
    goal = inputs.get("goal", "traffic")
    objective_map = {
        "traffic": "Traffic",
        "engagement": "Engagement",
        "conversions": "Sales/Conversions",
        "video views": "Video Views",
        "leads": "Leads",
        "awareness": "Awareness",
    }
    return {
        "Campaign Objective": objective_map.get(goal.lower(), "Traffic"),
        "Ad Sets": [
            "Core audience: interests + behaviors",
            "Retargeting: website visitors/video viewers/engagers",
            "Lookalike: customers, leads, or engaged fans when available",
        ],
        "Placements": ["Instagram Reels", "Instagram Stories", "Facebook Feed", "Instagram Feed"],
        "Optimization": "Start with lowest cost. Move to conversion optimization after enough data.",
        "Creative": creative or "Generate copy in Creative Studio.",
        "KPIs": ["CTR", "CPC", "CPM", "CPA", "Conversion rate", "Engagement rate"],
    }
