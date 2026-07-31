from enum import Enum
from core.event_bus import EventBus
from utils.logger import get_logger

logger = get_logger("LifecycleManager")

class SystemState(Enum):
    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    SLEEPING = "SLEEPING"
    SHUTTING_DOWN = "SHUTTING_DOWN"

class LifecycleManager:
    """
    Manages the core lifecycle and state of the VIRA assistant.
    Broadcasts state changes over the EventBus.
    """
    def __init__(self, event_bus: EventBus):
        self.state = SystemState.INITIALIZING
        self.event_bus = event_bus
        logger.info("LifecycleManager initialized.")

    async def start(self):
        logger.info("Starting up VIRA...")
        await self.set_state(SystemState.RUNNING)

    async def sleep(self):
        logger.info("Putting VIRA to sleep...")
        await self.set_state(SystemState.SLEEPING)

    async def wake(self):
        logger.info("Waking up VIRA...")
        await self.set_state(SystemState.RUNNING)

    async def shutdown(self):
        logger.info("Shutting down VIRA...")
        await self.set_state(SystemState.SHUTTING_DOWN)

    async def set_state(self, new_state: SystemState):
        if self.state != new_state:
            self.state = new_state
            # Broadcast the state change to all modules listening
            await self.event_bus.publish("system_state_changed", {"state": new_state.value})
