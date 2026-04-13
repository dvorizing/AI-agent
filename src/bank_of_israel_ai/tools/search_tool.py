"""Web search tool for procurement agent using CREWAI's SerperDevTool."""

from __future__ import annotations

import os
from typing import List, Dict
from crewai_tools import SerperDevTool


# Initialize Serper search tool for real Google searches
def _get_serper_tool():
    """Get or create SerperDevTool instance."""
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError(
            "SERPER_API_KEY not found in environment. "
            "Get one free at https://serper.dev (50 free searches/month)"
        )
    return SerperDevTool(api_key=api_key)


def search_web(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """Search the web using Google via Serper API (real web search).
    
    Uses CREWAI's SerperDevTool for actual Google search results.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return (default 3)
        
    Returns:
        List of dicts with url and title info
    """
    try:
        serper_tool = _get_serper_tool()
        
        # Search using Serper (real Google search)
        search_results = serper_tool.run(query)
        
        # Parse results
        results: List[Dict[str, str]] = []
        
        # Handle different response formats
        if isinstance(search_results, str):
            # If string response, try to extract URLs
            lines = search_results.split('\n')
            for line in lines:
                if line.strip().startswith('http'):
                    results.append({"url": line.strip(), "title": "Search Result"})
                    if len(results) >= max_results:
                        break
        elif isinstance(search_results, dict):
            # If dict response (JSON format)
            organic_results = search_results.get('organic', [])
            for result in organic_results[:max_results]:
                results.append({
                    "url": result.get("link", ""),
                    "title": result.get("title", ""),
                    "snippet": result.get("snippet", "")
                })
        elif isinstance(search_results, list):
            # If list of results
            for result in search_results[:max_results]:
                if isinstance(result, dict):
                    results.append({
                        "url": result.get("url") or result.get("link", ""),
                        "title": result.get("title", "")
                    })
                else:
                    results.append({"url": str(result), "title": "Result"})
        
        return results
        
    except Exception as e:
        print(f"Search error: {e}")
        return []
