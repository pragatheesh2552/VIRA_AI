import asyncio
from typing import Callable, Dict, List, Any
from utils.logger import get_logger

logger = get_logger("EventBus")

class EventBus:
    """
    Asynchronous Event Bus for decoupled Pub/Sub communication between modules.
    """
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe a callback function to a specific event type."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        if callback not in self.subscribers[event_type]:
            self.subscribers[event_type].append(callback)
            logger.debug(f"Subscribed to event: '{event_type}'")

    def unsubscribe(self, event_type: str, callback: Callable):
        """Unsubscribe a callback function from a specific event type."""
        if event_type in self.subscribers:
            try:
                self.subscribers[event_type].remove(callback)
                logger.debug(f"Unsubscribed from event: '{event_type}'")
            except ValueError:
                pass

    async def publish(self, event_type: str, payload: Any = None):
        """Publish an event with an optional payload to all subscribers."""
        logger.debug(f"Publishing event: '{event_type}' with payload: {payload}")
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                if asyncio.iscoroutinefunction(callback):
                    # Schedule async callbacks to run without blocking the publisher
                    asyncio.create_task(callback(payload))
                else:
                    # Run synchronous callbacks directly
                    callback(payload)
