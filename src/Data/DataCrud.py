from sqlalchemy.orm import Session
from Dto.DataDto import MailModel
from Models.DataModel import Mail

def add_to_mail(db:Session,mail:MailModel):
    existing_mail = db.query(Mail).filter(Mail.mail_id==mail.mail_id).first()
    if existing_mail:
        return existing_mail
    db.add(mail)
    db.commit()
    db.refresh(mail)
    return mail

def retrieve_mail_by_id(db:Session,id:str):
    result=db.query(Mail.summary).filter(Mail.mail_id==id).first()
    return result

def retrieve_from_mail(db:Session):
    result=db.query(Mail).all()
    return result
