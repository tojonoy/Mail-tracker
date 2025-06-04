import os
import ezgmail
import os
import json

def initialize_gmail():

    creds_content = os.getenv("CREDENTIALS_JSON")
    with open("credentials.json", "w") as f:
        f.write(creds_content)
    if not os.path.exists('token.json'):
        print("Running ezgmail.init() for the first time...")
        ezgmail.init(
    credentialsFile='credentials.json',
    tokenFile='token.json',
)

    else:
        print("Gmail already initialized.")
