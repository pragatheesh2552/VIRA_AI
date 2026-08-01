import asyncio
import os
from dotenv import load_dotenv

from core.event_bus import EventBus
from core.lifecycle import LifecycleManager
from modules.router.models import RoutedCommandPayload
from modules.cognitive.engine import CognitiveEngine
from utils.logger import get_logger

# Load env variables (for the API key)
load_dotenv()
logger = get_logger("TestCognitive")

async def mock_cognitive_response_handler(payload):
    logger.info(f"\n[Mock Module] Received 'cognitive_response'!")
    logger.info(f"Original Prompt: {payload.original_prompt}")
    logger.info(f"Response: {payload.response_text}\n")
    
    # We exit the process here to end the test successfully if it works
    os._exit(0)

async def main():
    logger.info("=== Starting VIRA Cognitive Engine Test ===")
    
    # Check if API key is set
    if not os.getenv("GEMINI_API_KEY"):
        logger.error("GEMINI_API_KEY is not set in the environment or .env file.")
        logger.error("Please add it before running this test. (e.g. create a .env file)")
        return
        
    # 1. Initialize core components
    event_bus = EventBus()
    lifecycle = LifecycleManager(event_bus)
    
    # 2. Initialize Cognitive Engine
    cognitive_engine = CognitiveEngine(event_bus)
    
    # 3. Subscribe to the cognitive_response event to see the result
    event_bus.subscribe("cognitive_response", mock_cognitive_response_handler)
    
    # 4. Start lifecycle (background tasks if any)
    # Using asyncio.create_task so we don't block
    asyncio.create_task(lifecycle.start())
    
    # Give it a tiny bit of time to start up
    await asyncio.sleep(1)
    
    # 5. Simulate a routed command that IS cognitive
    logger.info("Simulating a 'command_routed' event (Category: Cognitive)...")
    payload = RoutedCommandPayload(original_text="Explain quantum computing in one sentence.", category="Cognitive")
    await event_bus.publish("command_routed", payload)
    
    # 6. Simulate a routed command that IS NOT cognitive (should be ignored)
    logger.info("Simulating a 'command_routed' event (Category: Automation)...")
    payload_ignored = RoutedCommandPayload(original_text="turn on the lights", category="Automation")
    await event_bus.publish("command_routed", payload_ignored)
    
    # Wait a few seconds for the API call to complete
    logger.info("Waiting for response from Gemini API...")
    await asyncio.sleep(10)
    
    logger.warning("Test finished but no response was received (or it took too long).")

if __name__ == "__main__":
    asyncio.run(main())
