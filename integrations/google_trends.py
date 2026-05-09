from __future__ import annotations
import pandas as pd

def get_google_trends(keyword: str, timeframe: str = "today 3-m", geo: str = "") -> dict:
    """Pull Google Trends data with pytrends. No fake data here."""
    if not keyword:
        raise ValueError("Enter a keyword, artist, brand, genre, product, or service.")

    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl="en-US", tz=360)
        pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop="")
        interest = pytrends.interest_over_time()
        related = pytrends.related_queries()
        region = pytrends.interest_by_region(resolution="COUNTRY", inc_low_vol=True, inc_geo_code=False)
        return {
            "interest_over_time": interest.reset_index() if isinstance(interest, pd.DataFrame) else pd.DataFrame(),
            "related_top": related.get(keyword, {}).get("top", pd.DataFrame()) if related else pd.DataFrame(),
            "related_rising": related.get(keyword, {}).get("rising", pd.DataFrame()) if related else pd.DataFrame(),
            "regional_interest": region.reset_index() if isinstance(region, pd.DataFrame) else pd.DataFrame(),
        }
    except Exception as e:
        raise RuntimeError(
            "Google Trends request failed. Pytrends can rate-limit or block some cloud environments. "
            f"Try again later, narrow the timeframe, or enable Demo Mode. Details: {e}"
        )
