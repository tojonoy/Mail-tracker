import ezgmail
import asyncio
from Data.DataCrud import add_to_mail,retrieve_mail_by_id
from sqlalchemy.orm import Session
from Services.TaskService import add_to_tasks
from Setup.GeminiSetup import get_gemini
from Data.database import get_db
from Dto.DataDto import MailModel
from Models.DataModel import Mail
from datetime import datetime
last_seen_timestamp :datetime = None # Initialize the last seen email ID
async def get_last_email_timestamp():
    """
    Asynchronously fetch the last email ID from unread messages in the inbox.
    """
    threads = ezgmail.unread()
    message_timestamps = [
        msg.timestamp for thread in threads for msg in thread.messages
    ]
    if message_timestamps:
        return max((message_timestamps))
    return None

async def fetch_new_emails():
    global last_seen_timestamp
    new_emails=[]
    try:
        db_gen= get_db()
        db = next(db_gen)
        threads=ezgmail.unread()
        for thread in threads:
            for msg in thread.messages:
                msg_timestamp = msg.timestamp
                if last_seen_timestamp and msg_timestamp<= last_seen_timestamp:
                    continue
                body = msg.body or ""
                if retrieve_mail_by_id(db, msg.id):
                        continue
                summary=get_gemini(body.strip())
                new_email=MailModel(
                    mail_id=msg.id,
                    sender=msg.sender,
                    summary=summary,
                    timestamp=msg_timestamp
                )
                new_email = Mail(**new_email.dict())
                new_emails.append(new_email)
                if new_email:
                    newm=add_to_mail(db,new_email)
                    if newm:
                        add_to_tasks(db, msg.id,summary,msg_timestamp)

        if new_emails:
            last_seen_timestamp = max(mail.timestamp for mail in new_emails)
    except Exception as e:
        print(f"Error fetching new emails: {e}")
    finally:
        db_gen.close()

async def background_email_adder():
    while True:
        await fetch_new_emails()
        await asyncio.sleep(30)   

