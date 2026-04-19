"""Email tool – sends search results via Gmail SMTP.

The recipient address is **never** hardcoded – it is always received from
the prompt at runtime.
"""

from __future__ import annotations

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from crewai.tools import tool
from dotenv import load_dotenv

load_dotenv()


@tool("send_email")
def send_email(to_email: str, subject: str, body: str) -> str:
    """Send an email with the search results via Gmail SMTP.

    Use this tool after searching for a product to email the top 3 results
    to the address provided in the prompt.

    Args:
        to_email: The recipient email address (provided in the user prompt).
        subject: The email subject line.
        body: The full email body text (the search results report).

    Returns:
        A confirmation message or an error description.
    """
    gmail_user = os.getenv("GMAIL_ADDRESS", "")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD", "")

    if not gmail_user or not gmail_password:
        return "❌ GMAIL_ADDRESS or GMAIL_APP_PASSWORD is not configured in .env"

    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = gmail_user
        msg["To"] = to_email
        msg["Subject"] = subject

        html_body = body.replace("\n", "<br>")
        msg.attach(MIMEText(body, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.send_message(msg)

        return f"✅ Email sent successfully to {to_email}"

    except Exception as exc:
        return f"❌ Failed to send email: {exc}"

