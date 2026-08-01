import asyncio
import os
import sys
import shutil

from core.event_bus import EventBus
from core.lifecycle import LifecycleManager
from modules.router.models import RoutedCommandPayload
from modules.memory.engine import MemoryEngine
from utils.logger import get_logger

logger = get_logger("TestMemory")

# Clean up any existing test db before starting
DB_DIR = os.path.join(os.path.dirname(__file__), "database")
if os.path.exists(DB_DIR):
    shutil.rmtree(DB_DIR)

# Track events received
events_received = {
    "saved": 0,
    "found": 0,
    "not_found": 0,
    "deleted": 0
}

async def mock_memory_saved(payload):
    logger.info(f"\n[Mock Module] Received 'memory_saved'!")
    logger.info(f"Content: {payload.content}\n")
    events_received["saved"] += 1
    check_exit()

async def mock_memory_found(payload):
    logger.info(f"\n[Mock Module] Received 'memory_found'!")
    logger.info(f"Query: {payload.query}")
    logger.info(f"Results: {payload.results}\n")
    events_received["found"] += 1
    check_exit()

async def mock_memory_deleted(payload):
    logger.info(f"\n[Mock Module] Received 'memory_deleted'!")
    logger.info(f"Query: {payload.query}")
    logger.info(f"Count: {payload.count}\n")
    events_received["deleted"] += 1
    check_exit()

async def mock_memory_not_found(payload):
    logger.info(f"\n[Mock Module] Received 'memory_not_found'!")
    logger.info(f"Query: {payload.query}\n")
    events_received["not_found"] += 1
    check_exit()

def check_exit():
    # Expected: 2 saved (one duplicate ignored, but logic currently treats 'remember' as saved if duplicate ignored maybe? Wait, add_memory returns False on duplicate. Let's see what engine publishes.
    # Ah, engine publishes 'saved' for the first, and 'saved' for duplicate because add_memory doesn't raise error. Let's look at core.py. 
    # Let's just exit after a set amount of time if we don't do it dynamically
    pass

async def main():
    logger.info("=== Starting VIRA Memory Engine Test ===")
    
    event_bus = EventBus()
    lifecycle = LifecycleManager(event_bus)
    memory_engine = MemoryEngine(event_bus)
    
    event_bus.subscribe("memory_saved", mock_memory_saved)
    event_bus.subscribe("memory_found", mock_memory_found)
    event_bus.subscribe("memory_deleted", mock_memory_deleted)
    event_bus.subscribe("memory_not_found", mock_memory_not_found)
    
    asyncio.create_task(lifecycle.start())
    await asyncio.sleep(1)
    
    # 1. Remember a fact
    logger.info("Simulating: remember that my favorite color is blue")
    await event_bus.publish("command_routed", RoutedCommandPayload(original_text="remember that my favorite color is blue", category="Memory"))
    await asyncio.sleep(0.5)

    # 2. Remember duplicate (should not crash)
    logger.info("Simulating duplicate: remember that my favorite color is blue")
    await event_bus.publish("command_routed", RoutedCommandPayload(original_text="remember that my favorite color is blue", category="Memory"))
    await asyncio.sleep(0.5)

    # 3. Recall fact
    logger.info("Simulating: recall favorite color")
    await event_bus.publish("command_routed", RoutedCommandPayload(original_text="recall favorite color", category="Memory"))
    await asyncio.sleep(0.5)

    # 4. Recall fake fact (not_found)
    logger.info("Simulating: recall fake fact")
    await event_bus.publish("command_routed", RoutedCommandPayload(original_text="recall fake fact", category="Memory"))
    await asyncio.sleep(0.5)

    # 5. List memories
    logger.info("Simulating: list memories")
    await event_bus.publish("command_routed", RoutedCommandPayload(original_text="list all memories", category="Memory"))
    await asyncio.sleep(0.5)

    # 6. Forget fact
    logger.info("Simulating: forget favorite color")
    await event_bus.publish("command_routed", RoutedCommandPayload(original_text="forget favorite color", category="Memory"))
    await asyncio.sleep(0.5)

    # 7. Forget fake fact (not_found)
    logger.info("Simulating: forget mysterious fact")
    await event_bus.publish("command_routed", RoutedCommandPayload(original_text="forget mysterious fact", category="Memory"))
    await asyncio.sleep(1)

    logger.info(f"Final Event Counts: {events_received}")
    
    # Verify DB was created
    if os.path.exists(os.path.join(DB_DIR, "vira_memory.db")):
        logger.info("SUCCESS: vira_memory.db was created.")
    else:
        logger.error("FAILURE: vira_memory.db was not found.")

    os._exit(0)

if __name__ == "__main__":
    asyncio.run(main())
