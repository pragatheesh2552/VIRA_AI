from core.event_bus import EventBus
from modules.vision.core import VisionCore
from modules.vision.models import VisionResponsePayload, VisionFailedPayload
from modules.vision.exceptions import VisionModuleError, ScreenshotError, GeminiVisionError
from utils.logger import get_logger

logger = get_logger("VisionEngine")

class VisionEngine:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.core = VisionCore()
        
        # Subscribe to command_routed events
        self.event_bus.subscribe("command_routed", self.handle_routed_command)
        logger.info("VisionEngine initialized and subscribed to 'command_routed'.")

    async def handle_routed_command(self, payload):
        """
        Callback for when a command is routed.
        Only processes commands with category 'Vision'.
        """
        try:
            category = payload.category if hasattr(payload, 'category') else payload.get("category", "")
            original_text = payload.original_text if hasattr(payload, 'original_text') else payload.get("original_text", "")
            
            if category != "Vision":
                # Ignore non-vision commands
                return
                
            logger.info(f"Vision Engine processing command: '{original_text}'")
            
            # Execute vision action
            try:
                # The core handles taking the screenshot and asking Gemini
                response_text = self.core.process_vision_prompt(original_text)
                
                # Publish completion (the TTS Engine will pick this up if we named it vision_response, wait, TTS doesn't subscribe to vision_response yet.
                # Actually we were instructed to publish "vision_response")
                response_payload = VisionResponsePayload(
                    original_command=original_text,
                    response_text=response_text
                )
                await self.event_bus.publish("vision_response", response_payload)
                logger.info(f"Published 'vision_response' event.")
                
            except (ScreenshotError, GeminiVisionError) as ve:
                logger.warning(f"Vision action failed: {ve}")
                failed_payload = VisionFailedPayload(
                    original_command=original_text,
                    reason=str(ve)
                )
                await self.event_bus.publish("vision_failed", failed_payload)
                
        except VisionModuleError as e:
            logger.error(f"Vision Module Error: {e}")
            await self.event_bus.publish("system_error", {"source": "vision", "error": str(e)})
        except Exception as e:
            logger.error(f"Unexpected error in Vision Engine: {e}")
