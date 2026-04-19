"""CrewAI procurement agent powered by Google Gemini.

One agent, one task, two tools:
  1. search_product – search the internet for a product
  2. send_email     – email the top-3 results
"""

from __future__ import annotations

import os
import sys
from typing import Optional

if sys.stdout.encoding != "utf-8":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from crewai import Agent, Crew, Process, Task, LLM
from dotenv import load_dotenv

from ..tools.search_tool import search_product
from ..tools.email_tool import send_email

os.environ.setdefault("CREWAI_TELEMETRY_OPT_IN", "false")
os.environ.setdefault("CREWAI_TELEMETRY_ENABLED", "false")


def _build_llm() -> LLM:
    """Create a CrewAI LLM backed by Google Gemini."""
    load_dotenv()

    api_key = os.getenv("GOOGLE_AI_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_AI_API_KEY is missing from .env")

    model_name = os.getenv("CREWAI_LLM", "gemini-2.5-flash").strip()
    print(f"🤖 Using Google Gemini ({model_name}) …")

    return LLM(
        model=f"gemini/{model_name}",
        api_key=api_key,
    )


def run_procurement_agent(
    prompt: str,
    env_path: Optional[str] = None,
) -> str:
    """Run the CrewAI procurement agent.

    The LLM parses the free-text prompt on its own – extracting the product
    name, email address, and any other details it needs.

    Args:
        prompt:   The raw user prompt (e.g. "מחשב נייד Dell ושלח ל-user@example.com").
        env_path: Optional path to the .env file.

    Returns:
        The agent's final output text.
    """
    if env_path:
        load_dotenv(env_path)
    else:
        load_dotenv()

    print(f"\n{'=' * 70}")
    print(f"📝  Prompt : {prompt}")
    print(f"{'=' * 70}\n")

    # --- LLM ---
    llm = _build_llm()

    # --- Agent ---
    agent = Agent(
        role="Procurement Specialist",
        goal=(
            "Search the internet for the requested product, find the top 3 "
            "results, and email them to the recipient."
        ),
        backstory=(
            "You are an expert procurement specialist. You receive a product "
            "name and an email address. You search the web for the product, "
            "pick the 3 best results, and send a clear report by email."
        ),
        tools=[search_product, send_email],
        verbose=True,
        llm=llm,
    )

    # --- Task ---
    task = Task(
        description=(
            f"The user sent this request:\n"
            f'"{prompt}"\n\n'
            f"Your job:\n"
            f'1. Figure out what product the user wants and use the "search_product" tool to search Google for it.\n'
            f"2. From the results, pick the top 3 most relevant results.\n"
            f"3. Prepare a short procurement report with the 3 results "
            f"   (title, link, description for each).\n"
            f"4. If the user provided an email address, use the \"send_email\" tool "
            f"   to send the report to that address.\n"
            f"   If no email was provided, skip the email step.\n"
            f"5. Return the report text as your final answer."
        ),
        expected_output=(
            "A procurement report listing the top 3 search results for the "
            "product, and confirmation that the email was sent (if an email address was provided)."
        ),
        agent=agent,
    )

    # --- Crew ---
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    print("⏳ Running procurement agent …\n")

    try:
        result = crew.kickoff()
        result_text = str(result)
    except Exception as exc:
        result_text = f"❌ Agent error: {exc}"

    print(f"\n{'=' * 70}")
    print("✅  Done")
    print(f"{'=' * 70}\n")
    return result_text

