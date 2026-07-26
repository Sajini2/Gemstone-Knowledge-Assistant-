"""
Gemstone Knowledge Assistant - Configuration Helper
Manages environment variables, Groq API Key, OpenRouter API Key, and Streamlit secrets.
"""

import os
from dotenv import load_dotenv

# Load local .env file if present
load_dotenv()


def get_api_key(key_name: str = "GROQ_API_KEY") -> str | None:
    """
    Retrieves API key by name from environment variables or Streamlit secrets.
    Checks GROQ_API_KEY and OPENROUTER_API_KEY.
    
    Args:
        key_name: Name of environment variable ("GROQ_API_KEY" or "OPENROUTER_API_KEY").
        
    Returns:
        String API key if configured, else None.
    """
    # 1. Check OS Environment Variables (from .env or system environment)
    key_value = os.getenv(key_name)
    if key_value and key_value.strip() and not key_value.startswith("gsk_your_") and not key_value.startswith("sk-or-your_"):
        return key_value.strip()

    # 2. Check Streamlit Secrets (for Streamlit Cloud or local .streamlit/secrets.toml)
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key_name in st.secrets:
            val = st.secrets[key_name]
            if val and str(val).strip():
                return str(val).strip()
    except Exception:
        pass

    return None
