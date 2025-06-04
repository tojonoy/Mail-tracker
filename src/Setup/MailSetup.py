import os
import ezgmail

def initialize_gmail():
    if os.getenv("RUNNING_ON_RENDER"):
        credentials_file = '/opt/render/project/src/credentials.json'
        token_file = '/opt/render/project/src/token.pickle'  # Use the pickle path
    else:
        credentials_file = 'credentials.json'
        token_file = 'token.json'
    
    ezgmail.init(credentialsFile=credentials_file, tokenFile=token_file)
