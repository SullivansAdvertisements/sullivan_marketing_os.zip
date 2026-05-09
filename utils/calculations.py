from __future__ import annotations
import math
import pandas as pd

PLATFORM_DEFAULTS = {
    "Spotify": {"cpm": 6, "ctr": 0.015, "cvr": 0.08, "weight": 0.18},
    "Meta/Instagram": {"cpm": 11, "ctr": 0.012, "cvr": 0.035, "weight": 0.26},
    "Google Search": {"cpm": 18, "ctr": 0.045, "cvr": 0.05, "weight": 0.20},
    "YouTube Ads": {"cpm": 8, "ctr": 0.010, "cvr": 0.025, "weight": 0.24},
    "TikTok": {"cpm": 7, "ctr": 0.014, "cvr": 0.025, "weight": 0.12},
}

def recommend_platforms(niche: str, goal: str) -> list[str]:
    text = f"{niche} {goal}".lower()
    if any(x in text for x in ["music", "artist", "single", "album", "video", "spotify"]):
        return ["YouTube Ads", "Meta/Instagram", "Spotify", "TikTok", "Google Search"]
    if any(x in text for x in ["clothing", "streetwear", "ecommerce", "shopify"]):
        return ["Meta/Instagram", "TikTok", "Google Search", "YouTube Ads"]
    if any(x in text for x in ["local", "service", "home care", "contractor"]):
        return ["Google Search", "Meta/Instagram", "YouTube Ads"]
    return ["Meta/Instagram", "Google Search", "YouTube Ads", "TikTok"]

def budget_split(total_budget: float, platforms: list[str]) -> pd.DataFrame:
    if total_budget <= 0 or not platforms:
        return pd.DataFrame(columns=["Platform", "Budget", "Share"])
    weights = {p: PLATFORM_DEFAULTS.get(p, {"weight": 0.1})["weight"] for p in platforms}
    total_weight = sum(weights.values())
    rows = []
    for p in platforms:
        share = weights[p] / total_weight
        rows.append({"Platform": p, "Budget": round(total_budget * share, 2), "Share": round(share * 100, 1)})
    return pd.DataFrame(rows)

def estimate_metrics(split_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in split_df.iterrows():
        p = row["Platform"]
        budget = float(row["Budget"])
        d = PLATFORM_DEFAULTS.get(p, {"cpm": 10, "ctr": 0.015, "cvr": 0.03})
        impressions = int((budget / d["cpm"]) * 1000) if d["cpm"] else 0
        clicks = int(impressions * d["ctr"])
        conversions = max(0, int(clicks * d["cvr"]))
        views = int(impressions * 0.35) if "YouTube" in p or p in ["TikTok", "Spotify"] else int(impressions * 0.12)
        rows.append({
            "Platform": p,
            "Budget": budget,
            "Est. Reach/Impressions": impressions,
            "Est. Clicks": clicks,
            "Est. Views/Streams": views,
            "Est. Conversions": conversions,
            "CTR": f"{d['ctr']*100:.2f}%",
            "CPM": f"${d['cpm']:.2f}",
        })
    return pd.DataFrame(rows)

def health_score(budget: float, has_research: bool, has_creative: bool, platforms: int) -> tuple[int, list[str]]:
    score = 35
    actions = []
    if budget >= 500:
        score += 15
    else:
        actions.append("Raise test budget to at least $500 so the platforms can learn.")
    if platforms >= 3:
        score += 15
    else:
        actions.append("Test at least 3 channels before scaling.")
    if has_research:
        score += 20
    else:
        actions.append("Run Google Trends research before finalizing targeting.")
    if has_creative:
        score += 15
    else:
        actions.append("Generate 5–10 ad angles before launch.")
    if budget >= 2000:
        actions.append("Use a 70/20/10 split: 70% proven targeting, 20% new audiences, 10% experiments.")
    else:
        actions.append("Start tight: one main offer, one main audience, two creative angles.")
    return min(score, 100), actions
