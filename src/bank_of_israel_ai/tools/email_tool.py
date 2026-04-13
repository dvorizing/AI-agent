"""Email sending utilities.

Simple email configuration helper.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


@dataclass
class EmailSettings:
    """Email configuration settings."""
    sendgrid_api_key: str
    from_address: str
    to_addresses: list[str]


def load_email_settings(env_path: Optional[str] = None) -> EmailSettings:
    """Load email settings from environment variables."""

    if env_path:
        load_dotenv(env_path)
    else:
        load_dotenv()

    def _get(key: str, required: bool = True) -> str:
        value = os.getenv(key)
        if required and not value:
            raise ValueError(f"Missing required environment variable: {key}")
        return value or ""

    sendgrid_api_key = _get("SENDGRID_API_KEY", required=False)
    from_address = _get("EMAIL_FROM", required=False)
    to_addresses_str = _get("EMAIL_TO", required=False)

    return EmailSettings(
        sendgrid_api_key=sendgrid_api_key,
        from_address=from_address,
        to_addresses=[addr.strip() for addr in to_addresses_str.split(",") if addr.strip()] if to_addresses_str else [],
    )


def send_email(subject: str, body: str, settings: EmailSettings) -> bool:
    """Send email using SendGrid (requires SendGrid API key).
    
    Args:
        subject: Email subject
        body: Email body
        settings: EmailSettings object
    
    Returns:
        True if sent successfully, False otherwise
    """
    # Try SendGrid first if API key present (and is not a dummy key)
    if settings.sendgrid_api_key and not "dummy" in settings.sendgrid_api_key.lower():
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail

            mail = Mail(
                from_email=settings.from_address,
                to_emails=settings.to_addresses,
                subject=subject,
                html_content=body,
            )

            sg = SendGridAPIClient(settings.sendgrid_api_key)
            response = sg.send(mail)

            if getattr(response, "status_code", None) in [200, 201, 202]:
                print(f"✅ Email sent successfully to {settings.to_addresses}")
                return True
            else:
                print(f"❌ Failed to send email via SendGrid: {getattr(response, 'status_code', response)}")
                # Fall through to try SMTP fallback below
        except ImportError:
            print("⚠️  SendGrid library not installed. Install with: pip install sendgrid")
        except Exception as e:
            print(f"❌ Error sending email via SendGrid: {e}")

    # SMTP fallback (if environment provides SMTP settings)
    smtp_host = os.getenv("SMTP_HOST")
    if smtp_host:
        try:
            smtp_port = int(os.getenv("SMTP_PORT", "587"))
            smtp_user = os.getenv("SMTP_USER")
            smtp_pass = os.getenv("SMTP_PASS")
            use_ssl = os.getenv("SMTP_USE_SSL", "false").lower() in ("1", "true", "yes")
            use_tls = os.getenv("SMTP_USE_TLS", "true").lower() in ("1", "true", "yes")

            from email.message import EmailMessage
            import smtplib

            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = settings.from_address
            msg["To"] = ", ".join(settings.to_addresses)
            msg.set_content(body)

            if use_ssl:
                server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30)
            else:
                server = smtplib.SMTP(smtp_host, smtp_port, timeout=30)

            server.ehlo()
            if use_tls and not use_ssl:
                server.starttls()
                server.ehlo()

            if smtp_user and smtp_pass:
                server.login(smtp_user, smtp_pass)

            server.send_message(msg)
            server.quit()
            print(f"✅ Email sent via SMTP to {settings.to_addresses}")
            return True
        except Exception as e:
            print(f"❌ SMTP send failed: {e}")

    # Preview mode: no valid send method available
    print("⚠️  No valid SendGrid key or SMTP configuration. Email not sent.")
    print(f"📧 Would send from: {settings.from_address} to: {settings.to_addresses}")
    print("--- Email body preview ---")
    print(body)
    print("--- End preview ---")
    return False
