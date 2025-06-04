import os
import ezgmail
import os
import json
import shutil

def initialize_gmail():
    shutil.copy('/etc/secrets/credentials.json', 'credentials.json')
    shutil.copy('/etc/secrets/token.pickle', 'token.pickle')
    print("Credentials and token files copied successfully.")
    ezgmail.init(credentialsFile='credentials.json', tokenFile='token.pickle')
    print("Gmail initialized successfully.")
