import asyncio
from core.event_bus import EventBus
from core.lifecycle import LifecycleManager
from utils.logger import get_logger

logger = get_logger("Main")

async def test_module_callback(payload):
    """A simple test callback mimicking a module listening to state changes."""
    logger.info(f"[Mock Module] Received 'system_state_changed' -> State is now: {payload.get('state')}")

async def main():
    logger.info("=== Starting VIRA Core Engine Test ===")
    
    # 1. Initialize core components
    event_bus = EventBus()
    lifecycle = LifecycleManager(event_bus)
    
    # 2. Subscribe a test module to lifecycle events
    event_bus.subscribe("system_state_changed", test_module_callback)
    
    # 3. Simulate state changes
    await lifecycle.start()
    await asyncio.sleep(1) # Wait a bit to simulate work
    
    # 4. Simulate an arbitrary event (e.g., Voice engine detected a command)
    await event_bus.publish("voice_command_detected", {"text": "turn on dark mode"})
    await asyncio.sleep(1)
    
    # 5. Simulate sleep mode
    await lifecycle.sleep()
    await asyncio.sleep(1)
    
    # 6. Shutdown
    await lifecycle.shutdown()
    
    # Give the async tasks a brief moment to finish logging
    await asyncio.sleep(0.5)
    logger.info("=== VIRA Core Engine Test Complete ===")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Process interrupted by user.")
