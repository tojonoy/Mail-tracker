import os
import ezgmail

def initialize_gmail():
    if os.getenv("RUNNING_ON_RENDER"):
        token_file = '/opt/render/project/src/token.pickle'  # Use the pickle path
    else:
        token_file = 'token.json'
    
    ezgmail.init(credentialsFile='credentials.json', tokenFile=token_file)
