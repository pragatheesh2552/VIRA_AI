from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

try:
    models = client.models.list()
    for m in models:
        print(m.name)
except Exception as e:
    print(f"Error: {e}")
