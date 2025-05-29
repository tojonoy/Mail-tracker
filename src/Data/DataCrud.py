from sqlalchemy.orm import Session
from Dto.DataDto import MailModel,TaskModel
from Models.DataModel import Mail,Tasks

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

def add_to_task(db:Session,task:TaskModel):
    exsisting_task = db.query(Tasks).filter(Tasks.mail_id==task.mail_id).first()
    if exsisting_task:
        return exsisting_task    
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def retrieve_tasks(db:Session):
    result=db.query(Tasks).all()
    return result