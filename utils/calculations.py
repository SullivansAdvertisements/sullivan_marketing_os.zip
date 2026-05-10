import pandas as pd

def recommend_platforms(niche: str):
    niche = niche.lower()
    if "music" in niche or "artist" in niche:
        return ["Spotify","Meta/Instagram","YouTube Ads","Google Search","TikTok"]
    return ["Meta/Instagram","Google Search","YouTube Ads"]

def budget_split(total_budget: float, platforms: list[str]) -> pd.DataFrame:
    weights = {
        "Spotify": .2,
        "Meta/Instagram": .28,
        "Google Search": .22,
        "YouTube Ads": .2,
        "TikTok": .1,
    }
    total = sum(weights.get(p,.1) for p in platforms)
    rows=[]
    for p in platforms:
        share = weights.get(p,.1)/total
        rows.append({
            "Platform": p,
            "Budget": round(total_budget*share,2),
            "Share %": round(share*100,1)
        })
    return pd.DataFrame(rows)
