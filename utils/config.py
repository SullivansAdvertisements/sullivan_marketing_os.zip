import os
import streamlit as st

def get_secret(name: str, default: str = "") -> str:
    """Read a key from Streamlit secrets first, then environment variables."""
    try:
        value = st.secrets.get(name, "")
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv(name, default)

def has_key(name: str) -> bool:
    value = get_secret(name, "")
    return bool(value and not value.lower().startswith(("your-", "sk-your", "paste-")))

def app_mode() -> str:
    return st.session_state.get("mode", "Demo Mode")
