import ezgmail
import asyncio
from Data.DataCrud import add_to_mail
from sqlalchemy.orm import Session
from Setup.GeminiSetup import get_gemini
from Data.database import get_db
from Dto.DataDto import MailModel
from Models.DataModel import Mail

last_seen_id = ""  # Initialize the last seen email ID
async def get_last_email_id():
    """
    Asynchronously fetch the last email ID from unread messages in the inbox.
    """
    threads = ezgmail.unread()
    message_ids = [
        msg.id for thread in threads for msg in thread.messages
    ]
    if message_ids:
        return max(message_ids)
    return ""

async def fetch_new_emails():
    global last_seen_id
    new_emails=[]
    try:
        db_gen= get_db()
        db = next(db_gen)
        threads=ezgmail.unread()
        for thread in threads:
            for msg in thread.messages:
                msg_id = msg.id
                if last_seen_id and msg_id<= last_seen_id:
                    continue
                summary=get_gemini(msg.body.strip())
                new_email=MailModel(
                    mail_id=msg_id,
                    sender=msg.sender,
                    summary=summary,
                    timestamp=msg.timestamp.isoformat()
                )
                new_email = Mail(**new_email.dict())
                new_emails.append(new_email)
                if new_email:
                    add_to_mail(db,new_email)
        if new_emails:
            last_seen_id = max(mail.id for mail in new_emails)
    except Exception as e:
        print(f"Error fetching new emails: {e}")
    finally:
        db_gen.close()

async def background_email_adder():
    while True:
        await fetch_new_emails()
        await asyncio.sleep(30)   

