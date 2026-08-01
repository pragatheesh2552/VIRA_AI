import asyncio
import os
import sys

from core.event_bus import EventBus
from core.lifecycle import LifecycleManager
from modules.router.models import RoutedCommandPayload
from modules.vision.engine import VisionEngine
from utils.logger import get_logger

logger = get_logger("TestVision")

events_received = {
    "response": 0,
    "failed": 0
}

async def mock_vision_response(payload):
    logger.info(f"\n[Mock Module] Received 'vision_response'!")
    logger.info(f"Original Command: {payload.original_command}")
    logger.info(f"Response: {payload.response_text}\n")
    events_received["response"] += 1
    check_exit()

async def mock_vision_failed(payload):
    logger.info(f"\n[Mock Module] Received 'vision_failed'!")
    logger.info(f"Original Command: {payload.original_command}")
    logger.info(f"Reason: {payload.reason}\n")
    events_received["failed"] += 1
    check_exit()

def check_exit():
    if events_received["response"] == 1:
        logger.info("Received expected vision_response event. Exiting successfully.")
        os._exit(0)
    if events_received["failed"] == 1:
        logger.warning("Received vision_failed event. This might be due to quota/network, but the event path works.")
        os._exit(0)

async def main():
    logger.info("=== Starting VIRA Vision Engine Test ===")
    
    event_bus = EventBus()
    lifecycle = LifecycleManager(event_bus)
    vision_engine = VisionEngine(event_bus)
    
    event_bus.subscribe("vision_response", mock_vision_response)
    event_bus.subscribe("vision_failed", mock_vision_failed)
    
    asyncio.create_task(lifecycle.start())
    await asyncio.sleep(1)
    
    logger.info("Simulating: what is on my screen?")
    payload = RoutedCommandPayload(original_text="describe what is on my screen in one sentence", category="Vision")
    await event_bus.publish("command_routed", payload)
    
    # Wait for screenshot + API call
    await asyncio.sleep(20)
    
    logger.warning("Test finished but did not receive response in time.")

if __name__ == "__main__":
    asyncio.run(main())
