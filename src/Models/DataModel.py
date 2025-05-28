from sqlalchemy import Column, Integer, String, DateTime, func
from Data.database import Base

class Mail(Base):

    __tablename__="Mails"

    id=Column(Integer, primary_key=True,index=True,autoincrement=True)
    mail_id=Column(String,nullable=False)
    sender=Column(String)
    summary=Column(String)
    timestamp=Column(DateTime,default=func.now())