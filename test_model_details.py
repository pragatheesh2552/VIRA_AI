from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

for m in client.models.list():
    if "gemini-2.5-flash" in m.name:
        print(m.name)
        print("Methods:", getattr(m, 'supported_generation_methods', getattr(m, 'supported_actions', 'None')))
