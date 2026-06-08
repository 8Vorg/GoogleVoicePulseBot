import smtplib
import os
import random
from email.mime.text import MIMEText
from datetime import datetime

def send_mail():
    # Credentials pulled dynamically from GitHub Secrets by the YAML workflow
    username = os.environ.get('GMAIL_USER')
    password = os.environ.get('GMAIL_PASSWORD')
    receiver = os.environ.get('GV_GATEWAY')

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
    msg['From'] = username
    msg['To'] = receiver

    try:
        # Connect to Google's standard SMTP server using App Passwords
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(username, password)
            server.sendmail(username, [receiver], msg.as_string())
        print(f"[{datetime.now()}] Successfully sent to: {receiver}")
    except Exception as e:
        print(f"Send failed: {e}")

if __name__ == "__main__":
    send_mail()
