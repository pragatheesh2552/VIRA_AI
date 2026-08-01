from google import genai
from google.genai import types
from modules.cognitive.config import COGNITIVE_CONFIG
from modules.cognitive.exceptions import GeminiAPIError
from utils.logger import get_logger

logger = get_logger("CognitiveCore")

class CognitiveCore:
    def __init__(self):
        self.api_key = COGNITIVE_CONFIG.get("api_key")
        self.system_instruction = COGNITIVE_CONFIG.get("system_instruction")
        
        if not self.api_key:
            logger.error("GEMINI_API_KEY is not set. Cognitive capabilities will not work.")
        else:
            # Initialize the client
            self.client = genai.Client(api_key=self.api_key)
            logger.info("CognitiveCore initialized.")

    def generate_response(self, prompt: str) -> str:
        """
        Generates a response from the Gemini API given a prompt.
        """
        if not self.api_key:
            raise GeminiAPIError("API key not configured.")
            
        if not prompt:
            logger.warning("Empty prompt provided to generate_response.")
            return ""
            
        logger.debug(f"Sending prompt to Gemini: '{prompt}'")
        
        # Exact API pattern from list_models.py: find supported models
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
            logger.error(f"Failed to fetch models for fallback: {e}")
            
        if not supported_models:
            raise GeminiAPIError("No models found that support generateContent.")

        # Try models until one succeeds
        for model_name in supported_models:
            try:
                logger.debug(f"Attempting to generate content with {model_name}...")
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=self.system_instruction,
                    )
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                # If this model fails (e.g. 404 not available to new users), log and try the next
                logger.debug(f"Model {model_name} failed: {e}. Trying next model...")
                continue
                
        logger.warning("All supported models failed to generate content.")
        return ""
