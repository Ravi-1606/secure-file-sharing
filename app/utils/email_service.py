import smtplib
from email.message import EmailMessage
import os

EMAIL = os.getenv("SMTP_EMAIL")
PASSWORD = os.getenv("SMTP_PASSWORD")

def send_verification_email(to_email, token):
    msg = EmailMessage()
    msg.set_content(f"Click to verify: http://localhost:8000/client/verify-email?token={token}")
    msg["Subject"] = "Verify your email"
    msg["From"] = EMAIL
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)
