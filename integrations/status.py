from utils.config import has_key

def integration_statuses():
    return {
        "OpenAI": has_key("OPENAI_API_KEY"),
        "SERPAPI": has_key("SERPAPI_API_KEY"),
        "Meta Ads": has_key("META_ACCESS_TOKEN") and has_key("META_AD_ACCOUNT_ID"),
        "Google Ads": has_key("GOOGLE_ADS_DEVELOPER_TOKEN"),
        "YouTube": has_key("YOUTUBE_API_KEY"),
        "Spotify": has_key("SPOTIFY_CLIENT_ID"),
    }
