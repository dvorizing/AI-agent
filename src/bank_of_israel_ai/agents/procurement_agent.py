"""CREWAI-based procurement agent with Google Gemini LLM.

This agent searches for the 3 cheapest price quotes and sends them via email.
"""
# encoding: utf-8

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Optional

# Ensure UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from crewai import Agent, Crew, Process, Task, LLM
from crewai.tools import tool
from dotenv import load_dotenv

from ..tools.email_tool import EmailSettings, load_email_settings, send_email
from ..tools.search_tool import search_web

# Disable CREWAI telemetry to avoid network timeouts
os.environ.setdefault("CREWAI_TELEMETRY_OPT_IN", "false")
os.environ.setdefault("CREWAI_TELEMETRY_ENABLED", "false")


@dataclass
class ProcurementRequest:
    """A user-provided procurement request."""

    query: str
    max_results: int = 10


# Custom tool for web searching with Serper
@tool
def search_product(query: str) -> str:
    """Search for product information using real Google search (Serper API).
    
    This tool uses CREWAI's SerperDevTool to perform real Google searches
    and returns actual supplier websites with titles and snippets.
    
    Args:
        query: The product to search for (e.g., 'Lenovo laptop', 'diamond chain', 'iPhone')
        
    Returns:
        Formatted list of top 3 search results with URLs and snippets
    """
    try:
        results = search_web(query, max_results=3)
        if not results:
            return f"No search results found for: {query}. Try a different search term."
        
        output = ["🔍 GOOGLE SEARCH RESULTS", "=" * 60]
        for i, result in enumerate(results, 1):
            url = result.get('url', result.get('link', 'N/A'))
            title = result.get('title', 'Untitled')
            snippet = result.get('snippet', '')
            
            output.append(f"\n#{i} - {title}")
            output.append(f"   Link: {url}")
            if snippet:
                output.append(f"   Preview: {snippet[:100]}...")
        
        output.append("\n" + "=" * 60)
        return "\n".join(output)
    except ValueError as e:
        # Serper API key not configured
        return f"Search not available: {e}\nPlease configure SERPER_API_KEY in .env file."
    except Exception as e:
        return f"Search error: {e}"


def create_procurement_agent():
    """Create a CREWAI agent for procurement with Google Gemini LLM.

    Configures a CREWAI `LLM` instance using the `GOOGLE_AI_API_KEY` (from
    Google AI Studio) and attaches it to the Agent so CREWAI sends LLM calls
    to Gemini instead of the OpenAI default.
    """

    # Load environment
    load_dotenv()

    # Get API key from environment
    api_key = os.getenv("GOOGLE_AI_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_AI_API_KEY not set in environment or .env file")

    # Create an LLM instance configured for Gemini. Use a Gemini model id
    # available to your Google AI Studio project (e.g. 'gemini-pro' or 'gemini-pro-vision').
    llm = LLM(
        model="gemini-pro",
        api_key=api_key,
        provider="google",
    )

    # Create the agent and attach the configured LLM instance
    agent = Agent(
        role="Procurement Specialist",
        goal=(
            "Find the 3 cheapest price quotes for products and prepare a professional report."
        ),
        backstory=(
            """You are an expert procurement specialist who specializes in finding
the best prices for products online. You search the internet, analyze prices, identify
the 3 cheapest options, and prepare professional reports for stakeholders."""
        ),
        tools=[search_product],
        verbose=True,
        llm=llm,
    )

    return agent


def create_search_task(agent: Agent, request: ProcurementRequest) -> Task:
    """Create a CREWAI task for finding product information via real Google search.
    
    Args:
        agent: The procurement agent
        request: The procurement request
        
    Returns:
        A CREWAI Task object
    """
    
    task_description = f"""You are searching for: "{request.query}"

Your task using REAL GOOGLE SEARCH (via Serper API):
1. Use the search_product tool to search Google for "{request.query}"
2. The tool will return real supplier/retailer search results
3. For each of the top 3 results, analyze:
   - The website and what it offers
   - Relevance to the request
   - How to purchase or get more info

4. Format your response as a professional procurement research report with:
   - Product searched: "{request.query}"
   - Top 3 search results with links
   - Brief analysis of each result
   - Recommendation on where to find the best information"""
    
    task = Task(
        description=task_description,
        expected_output="A professional procurement research report with the top 3 Google search results and analysis for the requested product.",
        agent=agent,
        tools=[search_product],
    )
    
    return task


def run_procurement_agent(
    request: ProcurementRequest,
    send_email_results: bool = False,
    env_path: Optional[str] = None,
) -> str:
    """Execute the procurement agent with CREWAI.
    
    Falls back to direct search if CREWAI fails.
    
    Args:
        request: The procurement request
        send_email_results: Whether to send results via email
        env_path: Optional path to .env file
        
    Returns:
        The formatted search results
    """
    
    # Load environment
    if env_path:
        load_dotenv(env_path)
    else:
        load_dotenv()
    
    print(f"\n{'='*80}")
    print(f"🔍 PROCUREMENT SEARCH: {request.query}")
    print(f"{'='*80}\n")
    
    # Try CREWAI first
    try:
        # Create agent and task
        agent = create_procurement_agent()
        task = create_search_task(agent, request)
        
        # Create and execute crew
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )
        
        # Run the crew
        print("⏳ Searching for pricing information...\n")
        result = crew.kickoff()
        
        # Format results
        results_text = str(result)
        
        print(f"\n{'='*80}")
        print("✅ SEARCH COMPLETE (CREWAI)")
        print(f"{'='*80}\n")
        print(results_text)
        
    except Exception as crewai_error:
        print(f"⚠️  CREWAI failed: {crewai_error}")
        print("Falling back to direct search...\n")
        results_text = _fallback_search(request)
    
    # Send email if requested
    if send_email_results:
        try:
            settings = load_email_settings(env_path)
            if settings.to_addresses:
                email_body = _format_email_body(request, results_text)
                send_email(
                    subject=f"Procurement Report: {request.query}",
                    body=email_body,
                    settings=settings
                )
        except Exception as e:
            print(f"⚠️  Error sending email: {e}")
    
    return results_text


def _fallback_search(request: ProcurementRequest) -> str:
    """Fallback direct search when CREWAI fails.
    
    Performs a simple web search and formats results without LLM.
    """
    print("🔎 Performing direct web search (no LLM)...\n")
    
    try:
        # Search multiple times to get diverse results
        results = search_web(request.query, max_results=15)
        
        if not results:
            return f"No search results found for: {request.query}"
        
        # Format results
        lines = [
            f"Search Results for: {request.query}",
            f"Total results found: {len(results)}",
            "",
            "Top results:",
        ]
        
        for i, result in enumerate(results[:5], 1):
            lines.append(f"{i}. {result.get('url', 'N/A')}")
        
        output = "\n".join(lines)
        print(f"\n{'='*80}")
        print("✅ SEARCH COMPLETE (FALLBACK)")
        print(f"{'='*80}\n")
        print(output)
        
        return output
        
    except Exception as e:
        error_msg = f"Fallback search error: {e}"
        print(error_msg)
        return error_msg


def _format_email_body(request: ProcurementRequest, results: str) -> str:
    """Format results for email.
    
    Args:
        request: The procurement request
        results: The search results
        
    Returns:
        Formatted email body
    """
    
    lines = [
        "=== PROCUREMENT REPORT ===",
        f"Product: {request.query}",
        "",
        "=== PRICING ANALYSIS ===",
        results,
        "",
        "=== END REPORT ===",
        "",
        "This is an automated procurement report generated by AI Procurement Agent.",
    ]
    
    return "\n".join(lines)
