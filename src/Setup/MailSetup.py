import ezgmail
import os

def initialize_gmail():
    token_file = '/etc/secrets/token.json'
    #credentials_file = '/opt/render/project/src/credentials.json'  # or wherever your credentials are

    if not os.path.exists(token_file):
        raise RuntimeError(f"token.json not found at {token_file}. Authenticate locally first and upload it to Render.")
    
    try:
        # Directly load the token without starting a browser
        ezgmail._loadToken(token_file)
        print("Gmail initialized successfully using token.json.")
    except Exception as e:
        raise RuntimeError(f"Failed to load Gmail token: {e}")
