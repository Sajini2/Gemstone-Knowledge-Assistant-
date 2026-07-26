"""
Gemstone Knowledge Assistant - Groq API Connection Test Script
Phase 1 Setup Verification
"""

import os
import sys
from dotenv import load_dotenv


def main():
    # Load environment variables from .env file
    load_dotenv()

    groq_api_key = os.getenv("GROQ_API_KEY")

    # Check if GROQ_API_KEY is set and non-empty
    if not groq_api_key or not groq_api_key.strip():
        print("=" * 60)
        print("[ERROR] GROQ_API_KEY is missing or empty.")
        print("Please copy '.env.example' to '.env' and set your GROQ_API_KEY.")
        print("Example: GROQ_API_KEY=gsk_your_actual_api_key_here")
        print("=" * 60)
        sys.exit(1)

    print("[INFO] GROQ_API_KEY detected. Initializing test connection to Groq API...")

    try:
        from langchain_groq import ChatGroq

        # Initialize Groq LLM client
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            groq_api_key=groq_api_key,
            temperature=0.0,
        )

        test_prompt = "Hello! Please confirm in one short sentence that the connection to the Groq API is active."
        print(f"[INFO] Sending test prompt to Groq model ('llama-3.3-70b-versatile')...")
        
        response = llm.invoke(test_prompt)

        print("\n" + "=" * 60)
        print("[SUCCESS] Groq API connection verified successfully!")
        print(f"Model Response: {response.content.strip()}")
        print("=" * 60)

    except Exception as exc:
        print("\n" + "=" * 60)
        print(f"[ERROR] Failed to connect to Groq API: {exc}")
        print("Please verify your GROQ_API_KEY and network connection.")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
