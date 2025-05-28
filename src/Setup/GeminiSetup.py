
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
client = genai.Client(api_key=f"{os.getenv('GOOGLE_API_KEY')}")

def get_gemini(body:str):    
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents="Summarize the following email:\n\n" + body
    )
    print(response.text)
    return response.text
