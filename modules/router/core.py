from modules.router.config import ROUTER_RULES
from modules.router.exceptions import ClassificationError
from utils.logger import get_logger

logger = get_logger("RouterCore")

class RouterCore:
    def __init__(self):
        logger.info("RouterCore initialized.")

    def classify(self, text: str) -> str:
        """
        Classifies the given text into one of the predefined categories.
        Uses a simple rule-based matching system against config.ROUTER_RULES.
        """
        if not text:
            return "Unknown"
            
        text_lower = text.lower().strip()
        
        try:
            # Check for matches in the rules
            for category, keywords in ROUTER_RULES.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        return category
                        
            # If no rules match
            return "Unknown"
        except Exception as e:
            logger.error(f"Error classifying text '{text}': {e}")
            raise ClassificationError(f"Classification failed: {e}")
