"""Test 1 – Verify LLM (Gemini) connection works."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from dotenv import load_dotenv

load_dotenv()


def test_gemini_connection():
    """Send a simple prompt to Gemini and verify we get a response."""
    import google.generativeai as genai

    api_key = os.getenv("GOOGLE_AI_API_KEY")
    assert api_key, "GOOGLE_AI_API_KEY is not set in .env"

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content("Say hello in one word.")
    text = response.text.strip()

    print(f"✅ Gemini response: {text}")
    assert len(text) > 0, "Gemini returned an empty response"


if __name__ == "__main__":
    print("=" * 50)
    print("Test 1: LLM Connection (Google Gemini)")
    print("=" * 50)
    try:
        test_gemini_connection()
        print("\n✅ LLM connection test PASSED")
    except Exception as e:
        print(f"\n❌ LLM connection test FAILED: {e}")
        sys.exit(1)
