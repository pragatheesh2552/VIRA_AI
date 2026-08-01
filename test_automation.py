import asyncio
import os
import sys

from core.event_bus import EventBus
from core.lifecycle import LifecycleManager
from modules.router.models import RoutedCommandPayload
from modules.automation.engine import AutomationEngine
from utils.logger import get_logger

logger = get_logger("TestAutomation")

completed_events = 0
failed_events = 0

async def mock_automation_completed(payload):
    global completed_events
    logger.info(f"\n[Mock Module] Received 'automation_completed'!")
    logger.info(f"Original Command: {payload.original_command}")
    logger.info(f"Action Taken: {payload.action_taken}\n")
    completed_events += 1
    check_exit()

async def mock_automation_failed(payload):
    global failed_events
    logger.info(f"\n[Mock Module] Received 'automation_failed'!")
    logger.info(f"Original Command: {payload.original_command}")
    logger.info(f"Reason: {payload.reason}\n")
    failed_events += 1
    check_exit()

def check_exit():
    # We expect 2 completions and 1 failure in this test
    if completed_events == 2 and failed_events == 1:
        logger.info("All expected events received. Exiting successfully.")
        os._exit(0)

async def main():
    logger.info("=== Starting VIRA Automation Engine Test ===")
    
    # 1. Initialize core components
    event_bus = EventBus()
    lifecycle = LifecycleManager(event_bus)
    
    # 2. Initialize Automation Engine
    automation_engine = AutomationEngine(event_bus)
    
    # 3. Subscribe to events to verify output
    event_bus.subscribe("automation_completed", mock_automation_completed)
    event_bus.subscribe("automation_failed", mock_automation_failed)
    
    # 4. Start lifecycle (background tasks if any)
    asyncio.create_task(lifecycle.start())
    await asyncio.sleep(1)
    
    # 5. Simulate opening a known app (Calculator)
    logger.info("Simulating: open calculator")
    payload1 = RoutedCommandPayload(original_text="open calculator", category="Automation")
    await event_bus.publish("command_routed", payload1)
    
    await asyncio.sleep(1)
    
    # 6. Simulate opening a known folder (Downloads)
    logger.info("Simulating: open downloads")
    payload2 = RoutedCommandPayload(original_text="open downloads folder please", category="Automation")
    await event_bus.publish("command_routed", payload2)
    
    await asyncio.sleep(1)
    
    # 7. Simulate an unknown command (should fail gracefully)
    logger.info("Simulating: open mysterious app")
    payload3 = RoutedCommandPayload(original_text="open mysterious app", category="Automation")
    await event_bus.publish("command_routed", payload3)
    
    # Wait for processing
    await asyncio.sleep(3)
    logger.warning("Test finished but did not receive all expected events.")

if __name__ == "__main__":
    asyncio.run(main())
