from __future__ import annotations
import time
import pandas as pd

TIMEFRAME_OPTIONS = {
    "Past 7 days": "now 7-d",
    "Past 30 days": "today 1-m",
    "Past 90 days": "today 3-m",
    "Past 12 months": "today 12-m",
    "Past 5 years": "today 5-y",
}

def _clean_keyword_list(raw: str) -> list[str]:
    parts = []
    for item in raw.replace("\n", ",").split(","):
        item = item.strip()
        if item and item.lower() not in [x.lower() for x in parts]:
            parts.append(item)
    return parts

def demo_trends(keyword: str, max_results: int = 50) -> dict:
    dates = pd.date_range(end=pd.Timestamp.today(), periods=24, freq="W")
    interest = pd.DataFrame({"date": dates, keyword: [18,20,25,27,26,30,34,37,40,42,45,48,50,54,55,57,60,63,66,68,72,74,78,82]})
    q = [f"{keyword} playlist", f"{keyword} promotion", f"{keyword} ads", f"{keyword} video", f"{keyword} marketing",
         f"best {keyword}", f"new {keyword}", f"{keyword} fans", f"{keyword} release strategy", f"{keyword} campaign"]
    related = pd.DataFrame({"query": (q * ((max_results//len(q))+1))[:max_results], "value": list(range(100, 100-max_results, -1))})
    rising = pd.DataFrame({"query": [f"rising {x}" for x in related["query"].head(max_results)], "value": ["Breakout"] + list(range(500, 500-max_results+1, -1))})
    region = pd.DataFrame({"geoName": ["United States","Canada","United Kingdom","Australia","Germany","Brazil","Mexico","Nigeria","South Africa","Netherlands"], keyword: [100,86,82,73,68,61,55,52,49,46]})
    yt = pd.DataFrame({"YouTube Idea": [f"{keyword} behind the scenes", f"{keyword} official video", f"{keyword} reaction", f"{keyword} short clip", f"{keyword} story ad"], "Intent": ["awareness","views","engagement","short-form","ad hook"]})
    return {"interest_over_time": interest, "related_top": related, "related_rising": rising, "regional_interest": region, "youtube_ideas": yt}

def get_google_trends(keyword: str, timeframe: str = "today 3-m", geo: str = "", max_results: int = 50, extra_keywords: str = "") -> dict:
    if not keyword:
        raise ValueError("Enter a keyword first.")

    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl="en-US", tz=360, timeout=(10, 25), retries=2, backoff_factor=0.2)

        keyword_batch = [keyword] + _clean_keyword_list(extra_keywords)
        keyword_batch = keyword_batch[:5]  # Google Trends supports up to 5 terms per payload.
        pytrends.build_payload(keyword_batch, cat=0, timeframe=timeframe, geo=geo, gprop="")
        interest = pytrends.interest_over_time()
        if isinstance(interest, pd.DataFrame) and "isPartial" in interest.columns:
            interest = interest.drop(columns=["isPartial"])

        related_raw = pytrends.related_queries()
        top_frames, rising_frames = [], []
        for kw in keyword_batch:
            pack = related_raw.get(kw, {}) if related_raw else {}
            top = pack.get("top", pd.DataFrame())
            rising = pack.get("rising", pd.DataFrame())
            if isinstance(top, pd.DataFrame) and not top.empty:
                top["source_keyword"] = kw
                top_frames.append(top)
            if isinstance(rising, pd.DataFrame) and not rising.empty:
                rising["source_keyword"] = kw
                rising_frames.append(rising)

        time.sleep(0.4)
        region = pytrends.interest_by_region(resolution="COUNTRY", inc_low_vol=True, inc_geo_code=False)

        related_top = pd.concat(top_frames, ignore_index=True).head(max_results) if top_frames else pd.DataFrame()
        related_rising = pd.concat(rising_frames, ignore_index=True).head(max_results) if rising_frames else pd.DataFrame()

        yt_terms = []
        for source in [related_top, related_rising]:
            if isinstance(source, pd.DataFrame) and "query" in source.columns:
                yt_terms.extend(source["query"].dropna().astype(str).tolist())
        if not yt_terms:
            yt_terms = [keyword, f"{keyword} video", f"{keyword} review", f"{keyword} tutorial"]
        youtube_ideas = pd.DataFrame({
            "YouTube Idea": [f"{term} video ad" for term in yt_terms[:max_results]],
            "Intent": ["search demand / content angle"] * min(len(yt_terms), max_results)
        })

        return {
            "interest_over_time": interest.reset_index() if isinstance(interest, pd.DataFrame) else pd.DataFrame(),
            "related_top": related_top,
            "related_rising": related_rising,
            "regional_interest": region.reset_index() if isinstance(region, pd.DataFrame) else pd.DataFrame(),
            "youtube_ideas": youtube_ideas,
        }
    except Exception as e:
        raise RuntimeError(
            "Google Trends request failed. Pytrends can rate-limit in cloud hosting. "
            "Try fewer keywords, shorter timeframe, or Demo Mode. "
            f"Details: {e}"
        )
