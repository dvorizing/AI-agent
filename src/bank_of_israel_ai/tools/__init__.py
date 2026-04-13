"""Tools used by the BankOfIsrael AI agents."""

from .email_tool import send_email, EmailSettings
from .search_tool import search_web

__all__ = [
    "send_email",
    "EmailSettings",
    "search_web",
]
