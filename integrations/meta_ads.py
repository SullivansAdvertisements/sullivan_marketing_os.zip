from __future__ import annotations
from utils.config import has_key, get_secret

def meta_status() -> dict:
    ready = has_key("META_ACCESS_TOKEN") and has_key("META_AD_ACCOUNT_ID")
    return {
        "ready": ready,
        "message": "Meta keys found." if ready else "Add META_ACCESS_TOKEN and META_AD_ACCOUNT_ID to enable live Meta Ads actions."
    }

def build_meta_payload(plan: dict) -> dict:
    """Safe planning payload. Live campaign creation should require review before POSTing to Meta."""
    return {
        "objective": plan.get("objective", "OUTCOME_TRAFFIC"),
        "daily_budget": plan.get("daily_budget", 20),
        "audience": plan.get("audience", {}),
        "placements": plan.get("placements", ["Facebook Feed", "Instagram Feed", "Instagram Reels", "Stories"]),
        "optimization_goal": plan.get("optimization_goal", "LINK_CLICKS"),
        "status": "PAUSED_FOR_REVIEW",
    }
