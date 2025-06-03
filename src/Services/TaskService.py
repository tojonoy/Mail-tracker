from Data.DataCrud import add_to_task
from Dto.DataDto import TaskModel
from Models.DataModel import Tasks,Mail
from Services.SmsService import send_message
from Setup.GeminiSetup import get_task_gemini
from datetime import datetime
import json
import re



def get_tasks_from_response(response:str):
    try:
        json_match=re.search(r"\[.*?\]",response,re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        pass
    return []

def add_to_tasks(db, msg_id:int,body:str,timestamp:datetime):
    response=get_task_gemini(body=body,timestamp=timestamp)
    tasks=get_tasks_from_response(response)
    for task in tasks:
        task_dto=TaskModel(mail_id=msg_id,task=task["task"],priority=task["priority"],due_date=task["due_date"])
        send_message(timestamp=task["due_date"],priority=task["priority"],message_body=task["task"])
        task_dto=Tasks(**task_dto.dict())
        task_resp=add_to_task(db,task_dto)
        print(task_resp)


