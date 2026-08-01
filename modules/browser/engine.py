from core.event_bus import EventBus
from modules.browser.core import BrowserCore
from modules.browser.models import BrowserCompletedPayload, BrowserFailedPayload
from modules.browser.exceptions import BrowserModuleError, InvalidURLError
from utils.logger import get_logger

logger = get_logger("BrowserEngine")

class BrowserEngine:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.core = BrowserCore()
        
        # Subscribe to command_routed events
        self.event_bus.subscribe("command_routed", self.handle_routed_command)
        logger.info("BrowserEngine initialized and subscribed to 'command_routed'.")

    async def handle_routed_command(self, payload):
        """
        Callback for when a command is routed.
        Only processes commands with category 'Browser'.
        """
        try:
            category = payload.category if hasattr(payload, 'category') else payload.get("category", "")
            original_text = payload.original_text if hasattr(payload, 'original_text') else payload.get("original_text", "")
            
            if category != "Browser":
                # Ignore non-browser commands
                return
                
            logger.info(f"Browser Engine processing command: '{original_text}'")
            
            # Execute browser action
            try:
                action_taken, url_opened = self.core.process_command(original_text)
                
                # Publish completion
                response_payload = BrowserCompletedPayload(
                    original_command=original_text,
                    url_opened=url_opened,
                    action_taken=action_taken
                )
                await self.event_bus.publish("browser_completed", response_payload)
                logger.info(f"Published 'browser_completed' event: {action_taken}")
                
            except InvalidURLError as iue:
                # Handle invalid URLs or unrecognized commands gracefully
                logger.warning(f"Browser action failed: {iue}")
                failed_payload = BrowserFailedPayload(
                    original_command=original_text,
                    reason=str(iue)
                )
                await self.event_bus.publish("browser_failed", failed_payload)
                
        except BrowserModuleError as e:
            logger.error(f"Browser Module Error: {e}")
            await self.event_bus.publish("system_error", {"source": "browser", "error": str(e)})
        except Exception as e:
            logger.error(f"Unexpected error in Browser Engine: {e}")
