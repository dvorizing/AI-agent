"""Web search tool for the procurement agent.

Uses Serper API (via crewai_tools.SerperDevTool) to perform real Google
searches.  The product name is **never** hardcoded – it is always received
from the prompt at runtime.
"""

from __future__ import annotations

import json
import os
from typing import Dict, List

from crewai.tools import tool
from dotenv import load_dotenv

load_dotenv()


@tool("search_product")
def search_product(query: str) -> str:
    """Search the internet for a product by name using Google (Serper API).

    Use this tool when you need to find suppliers, prices, or purchase options
    for a product.  Pass the product name as *query*.

    Args:
        query: The product name or search phrase (e.g. 'laptop Dell Latitude 5540').

    Returns:
        A formatted string with the top 3 search results (title, link, snippet).
    """
    import requests

    api_key = os.getenv("SERPER_API_KEY")
    if not api_key or api_key == "your-serper-api-key-here":
        return (
            "❌ SERPER_API_KEY is not configured. "
            "Get a free key at https://serper.dev and add it to your .env file."
        )

    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
    payload = json.dumps({"q": query, "num": 3})

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
    except Exception as exc:
        return f"❌ Search error: {exc}"

    organic: List[Dict] = data.get("organic", [])
    if not organic:
        return f"No results found for: {query}"

    lines = [f"🔍 Top 3 Google results for: «{query}»", "=" * 60]
    for idx, item in enumerate(organic[:3], 1):
        title = item.get("title", "N/A")
        link = item.get("link", "N/A")
        snippet = item.get("snippet", "")
        lines.append(f"\n#{idx}  {title}")
        lines.append(f"   🔗 {link}")
        if snippet:
            lines.append(f"   📝 {snippet[:150]}")
    lines.append("\n" + "=" * 60)
    return "\n".join(lines)

