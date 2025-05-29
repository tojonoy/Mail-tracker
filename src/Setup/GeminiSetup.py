
from google import genai
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
client = genai.Client(api_key=f"{os.getenv('GOOGLE_API_KEY')}")

def get_gemini(body:str):    
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents="Summarize the following email:\n\n" + body
    )
    print(response.text)
    return response.text
context_prompt=(
    "You will be given the content of an email and a timestamp.\n"
    "Your task is to analyze the content and check if it contains any task descriptions.\n"
    "If tasks are found which can be reminders, meetings, exams or important changes or even tasks, return a JSON array where each item has 'task' , 'priority' and'due_date' keys , for each  task along with their corresponding priority level: 'high', 'medium', or 'low' and due_date as the date expected for the task to be done.\n"
    "If there are no tasks, return an empty JSON.\n"
    "Return the response without any formatting \n"
)
def get_task_gemini(body:str,timestamp:datetime):
    dynamic_prompt = f"Email received at {timestamp}:\n\n{body}"
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            {
                "role": "user",
                "parts": [
                    {"text": context_prompt},
                    {"text": dynamic_prompt}
                ]
            }
        ]
    )
    print(response.text)
    return response.text
