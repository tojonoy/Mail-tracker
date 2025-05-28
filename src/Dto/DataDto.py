from pydantic import BaseModel,ConfigDict
from datetime import datetime


class MailModel(BaseModel):
    mail_id:str
    sender:str
    summary:str
    timestamp:datetime
