import requests
import pandas as pd
from typing import Dict, Any, List, Optional

SERPAPI_ENDPOINT = "https://serpapi.com/search.json"


class SerpApiError(RuntimeError):
    pass


def _clean_list(items: Any, limit: int = 20) -> List[str]:
    if not items:
        return []
    out = []
    if isinstance(items, list):
        for item in items:
            if isinstance(item, str):
                out.append(item)
            elif isinstance(item, dict):
                value = item.get("query") or item.get("title") or item.get("name") or item.get("value")
                if value:
                    out.append(str(value))
    return out[:limit]


def serpapi_get(api_key: str, params: Dict[str, Any], timeout: int = 35) -> Dict[str, Any]:
    if not api_key:
        raise SerpApiError("SERPAPI_API_KEY is missing. Add it in Streamlit secrets to use live research.")
    safe_params = {k: v for k, v in params.items() if v not in (None, "", [])}
    safe_params["api_key"] = api_key
    try:
        response = requests.get(SERPAPI_ENDPOINT, params=safe_params, timeout=timeout)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout as exc:
        raise SerpApiError("SerpApi timed out. Try a smaller search or check your internet connection.") from exc
    except requests.exceptions.HTTPError as exc:
        raise SerpApiError(f"SerpApi HTTP error {response.status_code}: {response.text[:500]}") from exc
    except requests.exceptions.RequestException as exc:
        raise SerpApiError(f"SerpApi connection error: {exc}") from exc
    except ValueError as exc:
        raise SerpApiError("SerpApi returned a response that was not valid JSON.") from exc

    if data.get("error"):
        raise SerpApiError(f"SerpApi error: {data.get('error')}")
    return data


def google_search_research(api_key: str, query: str, country: str = "us", num: int = 10) -> Dict[str, Any]:
    data = serpapi_get(api_key, {
        "engine": "google",
        "q": query,
        "gl": country.lower(),
        "hl": "en",
        "num": num,
    })
    organic = data.get("organic_results", []) or []
    rows = []
    for r in organic:
        rows.append({
            "title": r.get("title", ""),
            "link": r.get("link", ""),
            "snippet": r.get("snippet", ""),
            "position": r.get("position", ""),
        })
    return {
        "raw": data,
        "results_df": pd.DataFrame(rows),
        "related_searches": _clean_list(data.get("related_searches")),
        "people_also_ask": _clean_list(data.get("related_questions")),
        "summary": f"Found {len(rows)} Google search results for '{query}'.",
    }


def youtube_search_research(api_key: str, query: str, country: str = "us") -> Dict[str, Any]:
    data = serpapi_get(api_key, {
        "engine": "youtube",
        "search_query": query,
        "gl": country.lower(),
        "hl": "en",
    })
    video_results = data.get("video_results", []) or []
    rows = []
    for r in video_results[:20]:
        rows.append({
            "title": r.get("title", ""),
            "channel": (r.get("channel") or {}).get("name", "") if isinstance(r.get("channel"), dict) else r.get("channel", ""),
            "views": r.get("views", ""),
            "published": r.get("published_date", ""),
            "link": r.get("link", ""),
        })
    return {
        "raw": data,
        "results_df": pd.DataFrame(rows),
        "related_searches": _clean_list(data.get("related_searches")),
        "summary": f"Found {len(rows)} YouTube results for '{query}'.",
    }


def google_trends_research(api_key: str, query: str, country: str = "US", timeframe: str = "today 12-m") -> Dict[str, Any]:
    data = serpapi_get(api_key, {
        "engine": "google_trends",
        "q": query,
        "geo": country.upper(),
        "date": timeframe,
        "data_type": "TIMESERIES",
    })

    timeline = data.get("interest_over_time", {}).get("timeline_data", []) or data.get("timeline_data", []) or []
    trend_rows = []
    for point in timeline:
        date_label = point.get("date", "")
        values = point.get("values", [])
        if values and isinstance(values, list):
            for v in values:
                trend_rows.append({
                    "date": date_label,
                    "keyword": v.get("query", query),
                    "interest": v.get("value", 0),
                })
        else:
            trend_rows.append({
                "date": date_label,
                "keyword": query,
                "interest": point.get("value", 0),
            })

    related_data = serpapi_get(api_key, {
        "engine": "google_trends",
        "q": query,
        "geo": country.upper(),
        "date": timeframe,
        "data_type": "RELATED_QUERIES",
    })
    related_queries = []
    related = related_data.get("related_queries", {})
    if isinstance(related, dict):
        for _, bucket in related.items():
            if isinstance(bucket, dict):
                for item in (bucket.get("top") or []) + (bucket.get("rising") or []):
                    if isinstance(item, dict):
                        related_queries.append(item.get("query") or item.get("title") or "")
    related_queries = [x for x in related_queries if x]

    region_df = pd.DataFrame()
    try:
        region_data = serpapi_get(api_key, {
            "engine": "google_trends",
            "q": query,
            "geo": country.upper(),
            "date": timeframe,
            "data_type": "GEO_MAP_0",
        })
        geo_rows = []
        for row in region_data.get("interest_by_region", []) or []:
            values = row.get("values", [])
            geo_rows.append({
                "region": row.get("location", ""),
                "interest": values[0].get("value", 0) if values and isinstance(values[0], dict) else row.get("value", 0),
            })
        region_df = pd.DataFrame(geo_rows)
    except Exception:
        region_df = pd.DataFrame()

    return {
        "raw": data,
        "trend_df": pd.DataFrame(trend_rows),
        "related_searches": related_queries[:25],
        "region_df": region_df,
        "summary": f"Pulled Google Trends data through SerpApi for '{query}'.",
    }


def run_research(api_key: str, query: str, country: str, timeframe: str, platform_focus: str, search_type: str) -> Dict[str, Any]:
    query = query.strip()
    if not query:
        raise SerpApiError("Enter a keyword, artist, brand, product, or niche before running research.")

    if search_type == "trends":
        return google_trends_research(api_key, query, country.upper(), timeframe)
    if platform_focus.lower() == "youtube" or search_type in ["youtube", "music/video topic research"]:
        return youtube_search_research(api_key, query, country.lower())

    enriched_query = query
    if search_type == "competitor research":
        enriched_query = f"{query} competitors ads marketing examples"
    elif search_type == "keyword ideas":
        enriched_query = f"{query} keyword ideas customer intent"
    elif search_type == "audience intent":
        enriched_query = f"{query} audience intent problems wants buying journey"
    elif search_type == "content angle research":
        enriched_query = f"{query} content ideas angles trends"
    elif platform_focus.lower() == "music":
        enriched_query = f"{query} music promotion playlist video fans"

    return google_search_research(api_key, enriched_query, country.lower())