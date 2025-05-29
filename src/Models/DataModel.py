from sqlalchemy import Column, Integer, String, DateTime, func
from Data.database import Base

class Mail(Base):

    __tablename__="Mails"

    id=Column(Integer, primary_key=True,index=True,autoincrement=True)
    mail_id=Column(String,nullable=False)
    sender=Column(String)
    summary=Column(String)
    timestamp=Column(DateTime,default=func.now())


class Tasks(Base):
    
    __tablename__="Tasks_Table"

    id=Column(Integer, primary_key=True,index=True,autoincrement=True)
    mail_id=Column(String,nullable=False)
    task=Column(String,nullable=False)
    priority=Column(String,default="Low")
    due_date=Column(String)