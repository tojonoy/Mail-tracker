from datetime import datetime
from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)
def send_message(timestamp,priority,message_body):

    full_message = f"[{timestamp}] Priority: {priority} - {message_body}"
    message = client.messages.create(
        from_='+16187643445',  
        body=full_message,
        to='+919895033144'     
    )

    print("Message sent. SID:", message.sid)
