def build_meta_campaign(brand, offer, goal, budget, audience):
    return {
        "Objective": "Engagement or Video Views for cold music/content; Traffic or Sales for product campaigns; Leads for service offers.",
        "Ad Sets": [
            "Cold interest stack",
            "Lookalike/engaged audience if available",
            "Retargeting: video viewers, IG engagers, site visitors"
        ],
        "Interests": [audience, "similar brands/artists", "streetwear", "hip hop", "music videos", "Spotify", "YouTube", "online shopping"],
        "Placements": "Advantage+ placements, with separate creative checks for Reels, Stories, Feed, and Explore.",
        "Budget": f"${float(budget):,.2f} total, test 3-5 ad sets before scaling winners.",
        "Optimization": "Optimize for the event closest to your goal: views, landing page views, leads, purchases, or engagement.",
        "Primary Text": f"{brand} is pushing {offer}. Tap in now and see why people are paying attention.",
        "Headlines": [f"Discover {offer}", "Built to get attention", "Do not miss this drop"],
        "CTAs": ["Learn More", "Watch More", "Shop Now", "Sign Up"],
        "Checklist": ["Pixel/CAPI checked", "UTMs added", "3 creatives loaded", "audiences separated", "daily budget confirmed"]
    }