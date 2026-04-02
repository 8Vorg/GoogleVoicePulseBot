import os
import base64
import random
from datetime import datetime
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def send_mail():
    # OAuth 2.0 credentials pulled from GitHub Secrets
    client_id = os.environ.get('GCP_CLIENT_ID')
    client_secret = os.environ.get('GCP_CLIENT_SECRET')
    refresh_token = os.environ.get('GMAIL_REFRESH_TOKEN')
    receiver = os.environ.get('GV_GATEWAY')

    if not all([client_id, client_secret, refresh_token, receiver]):
        print("Error: Missing required OAuth secrets or Gateway address.")
        return

    # Construct the credentials object directly from the refresh token
    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret
    )

    msgs = [
        "Update: System is running smoothly.",
        "Reminder: Keep active and stay connected.",
        "Monthly check-in: Hello world!",
        "Status: All systems go."
    ]
    content = f"{random.choice(msgs)} | Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    # Create the standardized email message
    message = EmailMessage()
    message.set_content(content)
    message['To'] = receiver
    message['Subject'] = 'GV Maintenance'

    # The Gmail API requires a base64url encoded string
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'raw': encoded_message}

    try:
        # Build the Gmail API service and execute the send command
        service = build('gmail', 'v1', credentials=creds)
        send_message = service.users().messages().send(userId='me', body=create_message).execute()
        print(f"[{datetime.now()}] Successfully sent to: {receiver} (Message ID: {send_message.get('id')})")
    
    except Exception as e:
        print(f"Send failed: {e}")

if __name__ == "__main__":
    send_mail()
