from serpapi import GoogleSearch
import pandas as pd
import streamlit as st

TIMEFRAME_OPTIONS = {
    "Past 7 days": "now 7-d",
    "Past 30 days": "today 1-m",
    "Past 90 days": "today 3-m",
    "Past 12 months": "today 12-m",
    "Past 5 years": "today 5-y",
}

def get_google_trends(
    keyword: str,
    geo: str = "US",
    date: str = "today 3-m",
):

    keyword = keyword.strip()

    if not keyword:
        raise ValueError("Keyword required.")

    api_key = st.secrets.get("SERPAPI_API_KEY", "")

    if not api_key:
        raise RuntimeError("SERPAPI_API_KEY missing in Streamlit secrets.")

    params = {
        "engine": "google_trends",
        "q": keyword,
        "geo": geo or "US",
        "date": date,
        "api_key": api_key,
    }

    search = GoogleSearch(params)

    results = search.get_dict()

    # =========================================
    # INTEREST OVER TIME
    # =========================================

    timeline = []

    try:
        for item in results["interest_over_time"]["timeline_data"]:

            value = item["values"][0]["extracted_value"]

            timeline.append({
                "date": item["date"],
                "value": value,
            })

    except Exception:
        pass

    interest_df = pd.DataFrame(timeline)

    # =========================================
    # RELATED QUERIES
    # =========================================

    related_queries = []

    try:
        rising = results["related_queries"]["rising"]

        for item in rising:

            related_queries.append({
                "query": item["query"],
                "value": item.get("value", "Breakout"),
            })

    except Exception:
        pass

    related_df = pd.DataFrame(related_queries)

    # =========================================
    # REGIONAL INTEREST
    # =========================================

    regions = []

    try:

        for item in results["interest_by_region"]:

            regions.append({
                "region": item["location"],
                "value": item["extracted_value"],
            })

    except Exception:
        pass

    region_df = pd.DataFrame(regions)

    # =========================================
    # YOUTUBE IDEAS
    # =========================================

    yt_ideas = []

    if not related_df.empty:

        for q in related_df["query"].head(30):

            yt_ideas.append({
                "YouTube Idea": f"{q} video ad",
                "Intent": "search demand / content angle"
            })

    yt_df = pd.DataFrame(yt_ideas)

    return {
        "interest_over_time": interest_df,
        "related_queries": related_df,
        "regional_interest": region_df,
        "youtube_ideas": yt_df,
        "raw_results": results,
    }
