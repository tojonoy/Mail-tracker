import os
import ezgmail

def initialize_gmail():
    if not os.path.exists('token.json'):
        print("Running ezgmail.init() for the first time...")
        ezgmail.init(credentialsFile='credentials.json', tokenFile='token.json', scopes=['https://www.googleapis.com/auth/gmail.readonly'])
    else:
        print("Gmail already initialized.")
