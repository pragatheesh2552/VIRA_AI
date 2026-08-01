from core.event_bus import EventBus
from modules.automation.core import AutomationCore
from modules.automation.models import AutomationCompletedPayload, AutomationFailedPayload
from modules.automation.exceptions import AutomationModuleError, ActionFailedError
from utils.logger import get_logger

logger = get_logger("AutomationEngine")

class AutomationEngine:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.core = AutomationCore()
        
        # Subscribe to command_routed events
        self.event_bus.subscribe("command_routed", self.handle_routed_command)
        logger.info("AutomationEngine initialized and subscribed to 'command_routed'.")

    async def handle_routed_command(self, payload):
        """
        Callback for when a command is routed.
        Only processes commands with category 'Automation'.
        """
        try:
            # Handle both object and dict payloads
            category = payload.category if hasattr(payload, 'category') else payload.get("category", "")
            original_text = payload.original_text if hasattr(payload, 'original_text') else payload.get("original_text", "")
            
            if category != "Automation":
                # Ignore non-automation commands
                return
                
            logger.info(f"Automation Engine processing command: '{original_text}'")
            
            # Execute action
            try:
                success_message = self.core.execute_command(original_text)
                # Publish completion
                response_payload = AutomationCompletedPayload(
                    original_command=original_text,
                    action_taken=success_message
                )
                await self.event_bus.publish("automation_completed", response_payload)
                logger.info(f"Published 'automation_completed' event: {success_message}")
                
            except ActionFailedError as afe:
                # Handle missing apps or unsupported commands gracefully
                logger.warning(f"Automation action failed: {afe}")
                failed_payload = AutomationFailedPayload(
                    original_command=original_text,
                    reason=str(afe)
                )
                await self.event_bus.publish("automation_failed", failed_payload)
                
        except AutomationModuleError as e:
            logger.error(f"Automation Module Error: {e}")
            await self.event_bus.publish("system_error", {"source": "automation", "error": str(e)})
        except Exception as e:
            logger.error(f"Unexpected error in Automation Engine: {e}")
