#!/usr/bin/env python3
"""
Gmail SMTP sender for CSEE Messaging Tool.
Uses an App Password — no OAuth, no Google Cloud project needed.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(subject: str, body: str, recipients: list) -> list:
    """Send a plain-text email to each recipient. Returns list of failed addresses."""
    sender = os.getenv("GMAIL_SENDER")
    password = os.getenv("GMAIL_APP_PASSWORD")

    if not sender:
        raise ValueError("GMAIL_SENDER not set in .env")
    if not password:
        raise ValueError("GMAIL_APP_PASSWORD not set in .env")

    failed = []
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(sender, password)

        for recipient in recipients:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = sender
            msg["To"] = recipient
            msg.attach(MIMEText(body, "plain", "utf-8"))

            try:
                smtp.send_message(msg)
                print(f"  [email] sent to {recipient}")
            except Exception as e:
                print(f"  [email] failed for {recipient}: {e}")
                failed.append(recipient)

    return failed


if __name__ == "__main__":
    import sys
    recipients = sys.argv[1:] if len(sys.argv) > 1 else ["you@example.com"]
    send_email("Test — CSEE Messaging Tool", "This is a test email from the CSEE Messaging Tool.", recipients)
