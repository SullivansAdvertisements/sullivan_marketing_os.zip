import os
import streamlit as st

def get_secret(name: str, default: str = "") -> str:
    try:
        v = st.secrets.get(name, "")
        if v:
            return str(v)
    except Exception:
        pass
    return os.getenv(name, default)

def has_key(name: str) -> bool:
    v = get_secret(name, "")
    return bool(v and not v.lower().startswith(("your-", "paste-")))
