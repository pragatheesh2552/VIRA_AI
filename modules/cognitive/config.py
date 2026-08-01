import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration for the Cognitive Engine
COGNITIVE_CONFIG = {
    "model_name": os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    "system_instruction": "You are VIRA, an intelligent and helpful AI assistant. Keep responses concise and natural for voice synthesis.",
    "api_key": os.getenv("GEMINI_API_KEY", "")
}
