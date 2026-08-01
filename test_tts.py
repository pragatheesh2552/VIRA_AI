import asyncio
import os
import sys

from core.event_bus import EventBus
from core.lifecycle import LifecycleManager
from modules.tts.engine import TTSEngine

# Import payloads
from modules.automation.models import AutomationCompletedPayload
from modules.browser.models import BrowserCompletedPayload
from modules.memory.models import MemorySavedPayload

from utils.logger import get_logger

logger = get_logger("TestTTS")

async def main():
    logger.info("=== Starting VIRA TTS Engine Test ===")
    
    event_bus = EventBus()
    lifecycle = LifecycleManager(event_bus)
    tts_engine = TTSEngine(event_bus)
    
    asyncio.create_task(lifecycle.start())
    await asyncio.sleep(1)
    
    logger.info("Testing automation_completed...")
    payload1 = AutomationCompletedPayload(original_command="open calculator", action_taken="Opened application calculator")
    await event_bus.publish("automation_completed", payload1)
    
    await asyncio.sleep(2.5) # Wait for speech
    
    logger.info("Testing browser_completed...")
    payload2 = BrowserCompletedPayload(original_command="open youtube", url_opened="https://youtube.com", action_taken="Opened YouTube")
    await event_bus.publish("browser_completed", payload2)
    
    await asyncio.sleep(2.5) # Wait for speech
    
    logger.info("Testing memory_saved...")
    payload3 = MemorySavedPayload(content="my favorite color is blue")
    await event_bus.publish("memory_saved", payload3)
    
    # Wait enough time for the queue to process all speech
    await asyncio.sleep(3)
    
    logger.info("All TTS events published and (hopefully) spoken! Exiting successfully.")
    
    tts_engine.core.shutdown()
    os._exit(0)

if __name__ == "__main__":
    asyncio.run(main())
