import asyncio
from core.event_bus import EventBus
from modules.router.engine import RouterEngine
from utils.logger import get_logger

logger = get_logger("TestRouter")

class MockSpeechPayload:
    def __init__(self, text):
        self.text = text
        self.is_wake_word = True

async def mock_router_listener(payload):
    logger.info(f"\n======================================")
    logger.info(f"!!! ROUTER EVENT CAUGHT !!!")
    logger.info(f"Original Text: '{payload.original_text}'")
    logger.info(f"Category: {payload.category}")
    logger.info(f"======================================\n")

async def main():
    logger.info("1. Initializing Event Bus...")
    event_bus = EventBus()
    
    logger.info("2. Initializing Router Engine...")
    router_engine = RouterEngine(event_bus)
    
    logger.info("3. Subscribing to 'command_routed'...")
    event_bus.subscribe("command_routed", mock_router_listener)
    
    # Test cases
    test_commands = [
        "open chrome to google",
        "search python tutorial on youtube",
        "remember my birthday is tomorrow",
        "describe what you see on the screen",
        "who is the president of the moon?",
        "do a backflip" # Should be unknown
    ]
    
    logger.info("\n>>> STARTING ROUTER TESTS <<<")
    
    for cmd in test_commands:
        logger.info(f"--- Simulating Speech: '{cmd}' ---")
        mock_payload = MockSpeechPayload(text=cmd)
        await event_bus.publish("speech_recognized", mock_payload)
        await asyncio.sleep(0.5) # Give the event bus time to process
        
    logger.info("\n>>> TESTS COMPLETE <<<")

if __name__ == "__main__":
    asyncio.run(main())
