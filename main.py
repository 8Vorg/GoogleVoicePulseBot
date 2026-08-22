import smtplib
import os
import random
from email.mime.text import MIMEText
from datetime import datetime

def send_mail():
    # Credentials pulled dynamically from GitHub Secrets
    username = os.environ.get('GMAIL_USER')
    password = os.environ.get('GMAIL_PASSWORD')
    receiver = os.environ.get('GV_GATEWAY')
    
    # Optional overrides for SMTP Relay routing
    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    envelope_sender = os.environ.get('ENVELOPE_SENDER', username)

    if not all([username, password, receiver]):
        print("Error: Missing GMAIL_USER, GMAIL_PASSWORD, or GV_GATEWAY secrets.")
        return

    msgs = [
        "Update: System is running smoothly.",
        "Reminder: Keep active and stay connected.",
        "Monthly check-in: Hello world!",
        "Status: All systems go."
    ]
    content = f"{random.choice(msgs)} | Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    # Construct the message payload
    msg = MIMEText(content)
    msg['Subject'] = 'GV Maintenance'
    msg['From'] = envelope_sender
    msg['To'] = receiver

    try:
        # Connect to defined SMTP server using App Passwords
        with smtplib.SMTP_SSL(smtp_host, 465) as server:
            server.login(username, password)
            server.sendmail(envelope_sender, [receiver], msg.as_string())
        print(f"[{datetime.now()}] Successfully sent to: {receiver}")
    except Exception as e:
        print(f"Send failed: {e}")

if __name__ == "__main__":
    send_mail()
