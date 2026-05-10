from utils.config import has_key

def integration_statuses():
    return {
        "OpenAI": has_key("OPENAI_API_KEY"),
        "Meta Ads": has_key("META_ACCESS_TOKEN") and has_key("META_AD_ACCOUNT_ID"),
        "Google Ads": all(has_key(k) for k in [
            "GOOGLE_ADS_DEVELOPER_TOKEN", "GOOGLE_ADS_CLIENT_ID", "GOOGLE_ADS_CLIENT_SECRET",
            "GOOGLE_ADS_REFRESH_TOKEN", "GOOGLE_ADS_LOGIN_CUSTOMER_ID"
        ]),
        "YouTube": has_key("YOUTUBE_API_KEY"),
        "Spotify": has_key("SPOTIFY_CLIENT_ID") and has_key("SPOTIFY_CLIENT_SECRET"),
    }
