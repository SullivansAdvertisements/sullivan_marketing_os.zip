import pandas as pd

PLATFORM_DEFAULTS = {
    "Spotify": {"cpm": 6, "ctr": 0.015, "cvr": 0.08, "weight": 0.18},
    "Meta/Instagram": {"cpm": 11, "ctr": 0.012, "cvr": 0.035, "weight": 0.27},
    "Google Search": {"cpm": 18, "ctr": 0.045, "cvr": 0.05, "weight": 0.20},
    "YouTube Ads": {"cpm": 8, "ctr": 0.010, "cvr": 0.025, "weight": 0.23},
    "TikTok": {"cpm": 7, "ctr": 0.014, "cvr": 0.025, "weight": 0.12},
}

def recommend_platforms(niche: str, goal: str) -> list[str]:
    text = f"{niche} {goal}".lower()
    if any(x in text for x in ["music", "artist", "single", "album", "video", "spotify"]):
        return ["YouTube Ads", "Meta/Instagram", "Spotify", "TikTok", "Google Search"]
    if any(x in text for x in ["clothing", "streetwear", "ecommerce", "shopify"]):
        return ["Meta/Instagram", "TikTok", "Google Search", "YouTube Ads"]
    if any(x in text for x in ["local", "service", "home care"]):
        return ["Google Search", "Meta/Instagram", "YouTube Ads"]
    return ["Meta/Instagram", "Google Search", "YouTube Ads", "TikTok"]

def budget_split(total_budget: float, platforms: list[str]) -> pd.DataFrame:
    weights = {p: PLATFORM_DEFAULTS.get(p, {"weight": 0.1})["weight"] for p in platforms}
    total = sum(weights.values()) or 1
    return pd.DataFrame([
        {"Platform": p, "Budget": round(total_budget * weights[p] / total, 2), "Share": round(weights[p] / total * 100, 1)}
        for p in platforms
    ])

def estimate_metrics(split_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in split_df.iterrows():
        p, budget = row["Platform"], float(row["Budget"])
        d = PLATFORM_DEFAULTS.get(p, {"cpm": 10, "ctr": .015, "cvr": .03})
        impressions = int((budget / d["cpm"]) * 1000)
        clicks = int(impressions * d["ctr"])
        conversions = int(clicks * d["cvr"])
        views = int(impressions * .36) if p in ["YouTube Ads", "TikTok", "Spotify"] else int(impressions * .12)
        rows.append({
            "Platform": p, "Budget": budget, "Est. Reach": impressions, "Est. Clicks": clicks,
            "Est. Views/Streams": views, "Est. Conversions": conversions,
            "CTR": f"{d['ctr']*100:.2f}%", "CPM": f"${d['cpm']:.2f}"
        })
    return pd.DataFrame(rows)

def health_score(budget: float, has_research: bool, has_creative: bool, platforms: int):
    score, actions = 35, []
    if budget >= 500: score += 15
    else: actions.append("Raise the test budget to at least $500 or keep the campaign very narrow.")
    if platforms >= 3: score += 15
    else: actions.append("Use at least 3 platforms before scaling.")
    if has_research: score += 20
    else: actions.append("Run Google Trends research before finalizing the launch.")
    if has_creative: score += 15
    else: actions.append("Generate multiple ad angles in Creative Studio.")
    if budget >= 2000:
        actions.append("Use 70% proven targeting, 20% new audiences, 10% experiments.")
    else:
        actions.append("Start focused: one offer, one audience, two creative angles.")
    return min(score, 100), actions
