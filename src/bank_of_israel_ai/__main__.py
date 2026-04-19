"""Main entry point for the Bank of Israel AI Procurement Agent.

Run via:
    python -m bank_of_israel_ai
"""

from .web_server import run_web

if __name__ == "__main__":
    run_web()
