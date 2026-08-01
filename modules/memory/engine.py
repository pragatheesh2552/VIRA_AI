from core.event_bus import EventBus
from modules.memory.core import MemoryCore
from modules.memory.models import (
    MemorySavedPayload,
    MemoryFoundPayload,
    MemoryDeletedPayload,
    MemoryNotFoundPayload
)
from modules.memory.exceptions import MemoryModuleError
from utils.logger import get_logger

logger = get_logger("MemoryEngine")

class MemoryEngine:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.core = MemoryCore()
        
        # Subscribe to command_routed events
        self.event_bus.subscribe("command_routed", self.handle_routed_command)
        logger.info("MemoryEngine initialized and subscribed to 'command_routed'.")

    async def handle_routed_command(self, payload):
        """
        Callback for when a command is routed.
        Only processes commands with category 'Memory'.
        """
        try:
            # Extract fields
            category = payload.category if hasattr(payload, 'category') else payload.get("category", "")
            original_text = payload.original_text if hasattr(payload, 'original_text') else payload.get("original_text", "")
            
            if category != "Memory":
                # Ignore non-memory commands
                return
                
            logger.info(f"Memory Engine processing command: '{original_text}'")
            
            # Process command
            action, data = self.core.process_command(original_text)
            
            # Publish appropriate event
            if action == "saved":
                event_payload = MemorySavedPayload(content=data["content"])
                await self.event_bus.publish("memory_saved", event_payload)
                
            elif action == "found":
                event_payload = MemoryFoundPayload(query=data["query"], results=data["results"])
                await self.event_bus.publish("memory_found", event_payload)
                
            elif action == "deleted":
                event_payload = MemoryDeletedPayload(query=data["query"], count=data["count"])
                await self.event_bus.publish("memory_deleted", event_payload)
                
            elif action == "not_found":
                event_payload = MemoryNotFoundPayload(query=data["query"])
                await self.event_bus.publish("memory_not_found", event_payload)
                
            logger.info(f"Published 'memory_{action}' event.")
                
        except MemoryModuleError as e:
            logger.error(f"Memory Module Error: {e}")
            await self.event_bus.publish("system_error", {"source": "memory", "error": str(e)})
        except Exception as e:
            logger.error(f"Unexpected error in Memory Engine: {e}")
