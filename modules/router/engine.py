from core.event_bus import EventBus
from modules.router.core import RouterCore
from modules.router.models import RoutedCommandPayload
from modules.router.exceptions import RouterModuleError
from utils.logger import get_logger

logger = get_logger("RouterEngine")

class RouterEngine:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.core = RouterCore()
        
        # Subscribe to speech_recognized events
        self.event_bus.subscribe("speech_recognized", self.handle_speech)
        logger.info("RouterEngine initialized and subscribed to 'speech_recognized'.")

    async def handle_speech(self, payload):
        """
        Callback for when speech is recognized.
        Extracts the text, classifies it, and publishes a command_routed event.
        """
        try:
            # Determine if payload is an object or dictionary
            text = payload.text if hasattr(payload, 'text') else payload.get("text", "")
            
            if not text:
                logger.warning("Received speech_recognized event with empty text. Ignoring.")
                return

            logger.info(f"Router received speech: '{text}'")
            
            # Classify the command
            category = self.core.classify(text)
            logger.info(f"Router classified command as: {category}")
            
            # Publish the routed command
            routed_payload = RoutedCommandPayload(original_text=text, category=category)
            await self.event_bus.publish("command_routed", routed_payload)
            
        except RouterModuleError as e:
            logger.error(f"Router Module Error: {e}")
            await self.event_bus.publish("system_error", {"source": "router", "error": str(e)})
        except Exception as e:
            logger.error(f"Unexpected error in Router Engine: {e}")
