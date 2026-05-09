from __future__ import annotations
from utils.config import has_key

REQUIRED = [
    "GOOGLE_ADS_DEVELOPER_TOKEN",
    "GOOGLE_ADS_CLIENT_ID",
    "GOOGLE_ADS_CLIENT_SECRET",
    "GOOGLE_ADS_REFRESH_TOKEN",
    "GOOGLE_ADS_LOGIN_CUSTOMER_ID",
]

def google_ads_status() -> dict:
    missing = [k for k in REQUIRED if not has_key(k)]
    return {
        "ready": not missing,
        "missing": missing,
        "message": "Google Ads credentials ready." if not missing else f"Missing: {', '.join(missing)}"
    }
