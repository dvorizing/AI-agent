"""Test 2 – Verify Gmail SMTP email sending works."""

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from dotenv import load_dotenv

load_dotenv()


def test_send_email():
    """Send a test email via Gmail SMTP."""
    gmail_user = os.getenv("GMAIL_ADDRESS")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    to_email = os.getenv("EMAIL_TO", "dvorizing@gmail.com")

    assert gmail_user, "GMAIL_ADDRESS is not set in .env"
    assert gmail_password and gmail_password != "PASTE_YOUR_APP_PASSWORD_HERE", \
        "GMAIL_APP_PASSWORD is not set in .env"

    msg = MIMEMultipart("alternative")
    msg["From"] = gmail_user
    msg["To"] = to_email
    msg["Subject"] = "Test – Bank of Israel AI Procurement Agent"

    body = "<h3>This is a test email from the AI Procurement Agent.</h3><p>If you received this, email sending works correctly.</p>"
    msg.attach(MIMEText(body, "html", "utf-8"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)

    print(f"✅ Email sent to {to_email}")


if __name__ == "__main__":
    print("=" * 50)
    print("Test 2: Email Sending (Gmail SMTP)")
    print("=" * 50)
    try:
        test_send_email()
        print("\n✅ Email sending test PASSED")
    except Exception as e:
        print(f"\n❌ Email sending test FAILED: {e}")
        sys.exit(1)
