import os
import ezgmail
import os
import json
import shutil

def initialize_gmail():
    shutil.copy('/etc/secrets/credentials.json', 'credentials.json')
    ezgmail.init(credentialsFile='credentials.json')  # Run locally
    return
    shutil.copy('/etc/secrets/credentials.json', 'credentials.json')
    shutil.copy('/etc/secrets/token.json', 'token.json')
    print("Credentials and token files copied successfully.")
    ezgmail.init(credentialsFile='credentials.json', tokenFile='token.json')
    print("Gmail initialized successfully.")
