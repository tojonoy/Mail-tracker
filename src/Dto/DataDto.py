from pydantic import BaseModel,ConfigDict
from datetime import datetime


class MailModel(BaseModel):
    mail_id:str
    sender:str
    summary:str
    timestamp:datetime
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )
class TaskModel(BaseModel):
    mail_id:str
    task :str 
    priority:str = "Low"
    due_date:str
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )
