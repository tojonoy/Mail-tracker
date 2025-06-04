import os
import ezgmail
import os
import json
import shutil

def initialize_gmail():

    creds_content = os.getenv("CREDENTIALS_JSON")
    token_path = "/etc/secrets/token.json"
    with open("credentials.json", "w") as f:
        f.write(creds_content)
    shutil.copy(token_path,"token.json")
    print("Initializing Gmail...")
    ezgmail.init(
    credentialsFile='credentials.json',
    tokenFile='token.json',
    )
    print("Gmail already initialized.")
