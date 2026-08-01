import os
from dotenv import load_dotenv

load_dotenv()

VISION_CONFIG = {
    # Reuse the same GEMINI_API_KEY from .env
    "api_key": os.getenv("GEMINI_API_KEY", ""),
    # Define a temporary path for screenshots
    "temp_screenshot_path": os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "temp", "screenshot.png"),
    "system_instruction": "You are VIRA, an intelligent AI with visual capabilities. Analyze the provided image and answer the user's prompt concisely."
}
