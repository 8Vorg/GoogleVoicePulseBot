from google_auth_oauthlib.flow import InstalledAppFlow

# We only need permission to send emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main():
    # Construct the client configuration dynamically
    client_config = {
        "installed": {
            "client_id": "YOUR_CLIENT_ID_HERE",
            "client_secret": "YOUR_CLIENT_SECRET_HERE",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"]
        }
    }

    print("Starting OAuth flow...")
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    
    # Force the consent screen to ensure a refresh_token is generated
    creds = flow.run_local_server(port=0, prompt='consent', access_type='offline')

    print("\n" + "="*50)
    print("SUCCESS! Capture the Refresh Token below:")
    print("="*50)
    print(f"\n{creds.refresh_token}\n")
    print("="*50)

if __name__ == '__main__':
    main()
