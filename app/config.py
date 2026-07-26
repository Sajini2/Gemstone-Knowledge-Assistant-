"""
Gemstone Knowledge Assistant - Central Configuration & Secrets Management
Provides helper for API key resolution across local environment (.env) and Streamlit Cloud (st.secrets).
"""

import os
from dotenv import load_dotenv

# Load local .env file if available
load_dotenv()


def get_api_key(key_name: str = "GROQ_API_KEY") -> str:
    """
    Retrieves API key from environment variables or Streamlit secrets fallback.
    
    Order of preference:
    1. OS Environment variable (via .env or system env)
    2. Streamlit Cloud Secrets (st.secrets)
    
    Args:
        key_name: Environment key name string (default: "GROQ_API_KEY").
        
    Returns:
        String API key or empty string if not configured.
    """
    # Check OS environment first
    api_key = os.getenv(key_name)
    if api_key and api_key.strip():
        return api_key.strip()

    # Fallback to Streamlit secrets if running in Streamlit environment
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key_name in st.secrets:
            secret_val = st.secrets[key_name]
            if secret_val and str(secret_val).strip():
                return str(secret_val).strip()
    except Exception:
        pass

    return ""
