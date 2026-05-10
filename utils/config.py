import os
import streamlit as st

def get_secret(name: str, default: str = "") -> str:
    try:
        value = st.secrets.get(name, "")
        if value:
            return str(value)
    except Exception:
        pass
    return os.getenv(name, default)

def has_key(name: str) -> bool:
    value = get_secret(name, "")
    return bool(value and not value.lower().startswith(("your-", "paste-", "sk-your", "sk-xxxx")))
