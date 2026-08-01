import os
from google import genai
from google.genai import types
from PIL import Image

from modules.vision.config import VISION_CONFIG
from modules.vision.exceptions import GeminiVisionError
from modules.vision.screenshot import ScreenCapture
from utils.logger import get_logger

logger = get_logger("VisionCore")

class VisionCore:
    def __init__(self):
        self.api_key = VISION_CONFIG.get("api_key")
        self.system_instruction = VISION_CONFIG.get("system_instruction")
        
        self.screen_capture = ScreenCapture()
        
        if not self.api_key:
            logger.error("GEMINI_API_KEY is not set. Vision capabilities will not work.")
        else:
            self.client = genai.Client(api_key=self.api_key)
            logger.info("VisionCore initialized.")

    def process_vision_prompt(self, prompt: str) -> str:
        """
        Takes a screenshot, passes it to the Gemini API alongside the prompt,
        and returns the description/answer.
        Uses a dynamic model fallback pattern to avoid deprecated models.
        """
        if not self.api_key:
            raise GeminiVisionError("API key not configured.")
            
        logger.info(f"Processing vision prompt: '{prompt}'")
        
        # 1. Capture screen
        img = self.screen_capture.capture()
        
        # 2. Fetch supported models dynamically
        supported_models = []
        try:
            for model in self.client.models.list():
                supported = False
                if hasattr(model, 'supported_generation_methods') and model.supported_generation_methods:
                    if 'generateContent' in model.supported_generation_methods:
                        supported = True
                elif hasattr(model, 'supported_actions') and model.supported_actions:
                    if 'generateContent' in model.supported_actions:
                        supported = True
                        
                if supported:
                    supported_models.append(model.name.replace("models/", "") if model.name else "Unknown")
        except Exception as e:
            logger.error(f"Failed to fetch models for Vision: {e}")
            
        if not supported_models:
            raise GeminiVisionError("No models found that support generateContent.")

        # 3. Try models until one successfully processes the image
        for model_name in supported_models:
            try:
                logger.debug(f"Attempting vision processing with {model_name}...")
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=[img, prompt],
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_instruction,
                    )
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                logger.debug(f"Vision Model {model_name} failed: {e}. Trying next model...")
                continue
                
        logger.error("All supported models failed to process the vision prompt.")
        raise GeminiVisionError("All supported models failed to process the image.")
