from typing import Dict


def allocate_budget(total_budget: float, platforms: list[str]) -> Dict[str, float]:
    if not platforms:
        return {}
    weights = {
        "Spotify": 0.18,
        "Meta / Instagram": 0.25,
        "Google Ads": 0.24,
        "YouTube Ads": 0.22,
        "Research & Tools": 0.11,
    }
    selected = {p: weights.get(p, 1 / len(platforms)) for p in platforms}
    total_weight = sum(selected.values()) or 1
    return {p: round(total_budget * w / total_weight, 2) for p, w in selected.items()}


def estimate_kpis(total_budget: float, goal: str = "Awareness") -> Dict[str, float]:
    cpc = 0.85 if total_budget < 2000 else 0.68
    cpm = 7.50 if total_budget < 2000 else 6.40
    cpv = 0.035 if "video" in goal.lower() else 0.05
    ctr = 2.1 if total_budget < 2000 else 2.7
    clicks = int(total_budget / cpc) if cpc else 0
    reach = int(total_budget / cpm * 1000) if cpm else 0
    views = int(total_budget / cpv) if cpv else 0
    conversions = int(clicks * 0.035)
    streams = int(total_budget / 0.04)
    saves = int(streams * 0.06)
    followers = int(streams * 0.018)
    return {
        "Estimated Reach": reach,
        "Estimated Clicks": clicks,
        "Estimated Views": views,
        "Estimated Streams": streams,
        "Estimated Leads/Conversions": conversions,
        "Estimated Saves": saves,
        "Estimated Followers": followers,
        "CPC": round(cpc, 2),
        "CPM": round(cpm, 2),
        "CTR": round(ctr, 2),
        "CPA": round(total_budget / max(conversions, 1), 2),
        "ROAS": round(2.0 + min(total_budget / 5000, 2.5), 2),
        "Cost Per View": round(cpv, 3),
        "Engagement Rate": round(4.5 + min(total_budget / 4000, 3), 2),
        "Campaign Health Score": min(98, int(74 + total_budget / 500)),
    }


def daily_budget(total_budget: float, timeframe_days: int) -> float:
    return round(total_budget / max(timeframe_days, 1), 2)