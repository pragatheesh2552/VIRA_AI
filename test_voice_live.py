import asyncio
from core.event_bus import EventBus
from modules.voice.engine import VoiceEngine
from utils.logger import get_logger

logger = get_logger("TestVoiceLive")

async def mock_event_listener(payload):
    logger.info(f"\n======================================")
    logger.info(f"!!! EVENT BUS CAUGHT AN EVENT !!!")
    logger.info(f"Type: speech_recognized")
    logger.info(f"Text: '{payload.text}'")
    logger.info(f"Is Wake Word?: {payload.is_wake_word}")
    logger.info(f"Confidence: {payload.confidence}")
    logger.info(f"======================================\n")

async def main():
    logger.info("1. Initializing Event Bus...")
    event_bus = EventBus()
    
    logger.info("2. Initializing Voice Engine...")
    voice_engine = VoiceEngine(event_bus)
    
    logger.info("3. Subscribing to 'speech_recognized'...")
    event_bus.subscribe("speech_recognized", mock_event_listener)
    
    logger.info("4. Starting Voice Engine loop...")
    # Run the voice engine in the background
    engine_task = asyncio.create_task(voice_engine.run())
    
    logger.info("\n>>> LISTENING FOR 30 SECONDS <<<")
    logger.info("Please speak into your microphone. Say 'VIRA, what is the weather?'")
    
    # Wait for 30 seconds to allow you to test
    await asyncio.sleep(30)
    
    logger.info("\n>>> TEST COMPLETE. SHUTTING DOWN <<<")
    # Stop the loop
    voice_engine.is_running = False
    await asyncio.sleep(1) # give it a moment to stop gracefully

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user.")
