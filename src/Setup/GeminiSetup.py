
from google import genai
from openai import OpenAI
import os
import ollama
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
client1 = genai.Client(api_key=f"{os.getenv('GOOGLE_API_KEY')}")
CHUNK_SIZE = 3000
OLLAMA_MODEL = "llama3"
def chunk_text(text, chunk_size=CHUNK_SIZE):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
def summarize_chunk(chunk, model=OLLAMA_MODEL):
    prompt = f"Summarize the following email:\n\n{chunk}"
    try:
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        return response['message']['content'].strip()
    except Exception as e:
        print(f"Error summarizing chunk: {e}")
        return "[Failed to summarize this chunk]"
def get_gemin(body:str):
    chunks = chunk_text(body)
    summaries = [summarize_chunk(chunk) for chunk in chunks]
    
    # Optional: Merge summaries into a final summary
    final_prompt = "Summarize the following points into a single cohesive summary:\n\n" + "\n".join(summaries)
    final_summary = summarize_chunk(final_prompt) if len(summaries) > 1 else summaries[0]
    print(final_summary)
    return final_summary

def get_gemini(body:str):    
    response = client1.models.generate_content(
        model="gemini-1.5-flash", contents="Summarize the following email:\n\n" + body
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
def get_task_gemii(body: str, timestamp: datetime):
    dynamic_prompt = f"Email received at {timestamp}:\n\n{body}"
    full_prompt = context_prompt + "\n" + dynamic_prompt

    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        )
        content = response['message']['content'].strip()
        print(content)
        return content
    except Exception as e:
        print(f"Error: {e}")
        return "[]"
def get_task_gemini(body:str,timestamp:datetime):
    dynamic_prompt = f"Email received at {timestamp}:\n\n{body}"
    
    response = client1.models.generate_content(
        model="gemini-1.5-flash",
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
client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        default_headers={
            "X-Title": "Mail-Tracker"
        }
    )
def get_openai(body: str) -> str:
    prompt = f"Summarize the following email:\n\n{body}"

    response = client.chat.completions.create(
        model="openai/gpt-4o", 
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    summary = response.choices[0].message.content
    print(summary)
    return summary
def get_task_openai(body:str,timestamp:datetime):

    dynamic_prompt = f"Email received at {timestamp}:\n\n{body}"
    
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "user", "content": context_prompt},
                {"role": "user", "content": dynamic_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error with task extraction: {e}")
        return "[]"