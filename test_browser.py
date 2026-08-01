import asyncio
import os
import sys

from core.event_bus import EventBus
from core.lifecycle import LifecycleManager
from modules.router.models import RoutedCommandPayload
from modules.browser.engine import BrowserEngine
from utils.logger import get_logger

logger = get_logger("TestBrowser")

events_received = {
    "completed": 0,
    "failed": 0
}

async def mock_browser_completed(payload):
    logger.info(f"\n[Mock Module] Received 'browser_completed'!")
    logger.info(f"Original Command: {payload.original_command}")
    logger.info(f"Action: {payload.action_taken}")
    logger.info(f"URL: {payload.url_opened}\n")
    events_received["completed"] += 1
    check_exit()

async def mock_browser_failed(payload):
    logger.info(f"\n[Mock Module] Received 'browser_failed'!")
    logger.info(f"Original Command: {payload.original_command}")
    logger.info(f"Reason: {payload.reason}\n")
    events_received["failed"] += 1
    check_exit()

def check_exit():
    # 3 completions, 1 failure
    if events_received["completed"] == 3 and events_received["failed"] == 1:
        logger.info("All expected events received. Exiting successfully.")
        os._exit(0)

async def main():
    logger.info("=== Starting VIRA Browser Engine Test ===")
    
    event_bus = EventBus()
    lifecycle = LifecycleManager(event_bus)
    browser_engine = BrowserEngine(event_bus)
    
    event_bus.subscribe("browser_completed", mock_browser_completed)
    event_bus.subscribe("browser_failed", mock_browser_failed)
    
    asyncio.create_task(lifecycle.start())
    await asyncio.sleep(1)
    
    # 1. Open known site
    logger.info("Simulating: open youtube")
    await event_bus.publish("command_routed", RoutedCommandPayload(original_text="open youtube", category="Browser"))
    await asyncio.sleep(1)

    # 2. Search
    logger.info("Simulating: search google for vira ai")
    await event_bus.publish("command_routed", RoutedCommandPayload(original_text="search google for vira ai", category="Browser"))
    await asyncio.sleep(1)

    # 3. Direct URL
    logger.info("Simulating: open python.org")
    await event_bus.publish("command_routed", RoutedCommandPayload(original_text="open python.org", category="Browser"))
    await asyncio.sleep(1)

    # 4. Unknown/Invalid
    logger.info("Simulating: open some random invalid thing")
    await event_bus.publish("command_routed", RoutedCommandPayload(original_text="open some random invalid thing", category="Browser"))
    await asyncio.sleep(2)
    
    logger.warning("Test finished but did not receive all expected events.")

if __name__ == "__main__":
    asyncio.run(main())
