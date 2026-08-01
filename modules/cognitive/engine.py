from core.event_bus import EventBus
from modules.cognitive.core import CognitiveCore
from modules.cognitive.models import CognitiveResponsePayload
from modules.cognitive.exceptions import CognitiveModuleError
from utils.logger import get_logger

logger = get_logger("CognitiveEngine")

class CognitiveEngine:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.core = CognitiveCore()
        
        # Subscribe to command_routed events
        self.event_bus.subscribe("command_routed", self.handle_routed_command)
        logger.info("CognitiveEngine initialized and subscribed to 'command_routed'.")

    async def handle_routed_command(self, payload):
        """
        Callback for when a command is routed.
        Only processes commands with category 'Cognitive'.
        """
        try:
            # Handle both object and dict payloads
            category = payload.category if hasattr(payload, 'category') else payload.get("category", "")
            original_text = payload.original_text if hasattr(payload, 'original_text') else payload.get("original_text", "")
            
            if category != "Cognitive":
                # Ignore non-cognitive commands
                return
                
            logger.info(f"Cognitive Engine processing command: '{original_text}'")
            
            # Generate response via Gemini
            response_text = self.core.generate_response(original_text)
            
            # Publish the response
            response_payload = CognitiveResponsePayload(
                original_prompt=original_text,
                response_text=response_text
            )
            await self.event_bus.publish("cognitive_response", response_payload)
            logger.info("Published 'cognitive_response' event.")
            
        except CognitiveModuleError as e:
            logger.error(f"Cognitive Module Error: {e}")
            await self.event_bus.publish("system_error", {"source": "cognitive", "error": str(e)})
        except Exception as e:
            logger.error(f"Unexpected error in Cognitive Engine: {e}")
