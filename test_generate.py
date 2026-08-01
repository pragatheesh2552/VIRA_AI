from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()
model_name = "gemini-flash-latest"

print(f"Testing generate_content with {model_name}...")
try:
    response = client.models.generate_content(
        model=model_name,
        contents="Hello, world!"
    )
    print("Response:", response.text)
except Exception as e:
    print("Error:", e)
