import asyncio
import os
import sys

# Core
from core.event_bus import EventBus
from core.lifecycle import LifecycleManager

# Modules
from modules.voice.engine import VoiceEngine
from modules.router.engine import RouterEngine
from modules.cognitive.engine import CognitiveEngine
from modules.automation.engine import AutomationEngine
from modules.memory.engine import MemoryEngine
from modules.browser.engine import BrowserEngine
from modules.vision.engine import VisionEngine
from modules.tts.engine import TTSEngine

from utils.logger import get_logger

logger = get_logger("VIRA_MAIN")

async def main():
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
        
    print("\n=== Starting VIRA ===")
    
    # 1. Initialize Core
    try:
        event_bus = EventBus()
        print("✓ EventBus")
    except Exception as e:
        logger.error(f"Failed to initialize EventBus: {e}")
        print("✗ EventBus Failed")
        return

    try:
        lifecycle = LifecycleManager(event_bus)
        print("✓ Lifecycle")
    except Exception as e:
        logger.error(f"Failed to initialize LifecycleManager: {e}")
        print("✗ Lifecycle Failed")
        return

    # 2. Initialize Modules gracefully
    modules = {}
    
    try:
        modules['voice'] = VoiceEngine(event_bus)
        print("✓ Voice")
    except Exception as e:
        logger.error(f"Voice Engine failed to initialize: {e}")
        print(f"✗ Voice Failed: {e}")

    try:
        modules['router'] = RouterEngine(event_bus)
        print("✓ Router")
    except Exception as e:
        logger.error(f"Router Engine failed to initialize: {e}")
        print(f"✗ Router Failed: {e}")

    try:
        modules['cognitive'] = CognitiveEngine(event_bus)
        print("✓ Cognitive")
    except Exception as e:
        logger.error(f"Cognitive Engine failed to initialize: {e}")
        print(f"✗ Cognitive Failed: {e}")

    try:
        modules['automation'] = AutomationEngine(event_bus)
        print("✓ Automation")
    except Exception as e:
        logger.error(f"Automation Engine failed to initialize: {e}")
        print(f"✗ Automation Failed: {e}")

    try:
        modules['memory'] = MemoryEngine(event_bus)
        print("✓ Memory")
    except Exception as e:
        logger.error(f"Memory Engine failed to initialize: {e}")
        print(f"✗ Memory Failed: {e}")

    try:
        modules['browser'] = BrowserEngine(event_bus)
        print("✓ Browser")
    except Exception as e:
        logger.error(f"Browser Engine failed to initialize: {e}")
        print(f"✗ Browser Failed: {e}")

    try:
        modules['vision'] = VisionEngine(event_bus)
        print("✓ Vision")
    except Exception as e:
        logger.error(f"Vision Engine failed to initialize: {e}")
        print(f"✗ Vision Failed: {e}")

    try:
        modules['tts'] = TTSEngine(event_bus)
        print("✓ TTS")
    except Exception as e:
        logger.error(f"TTS Engine failed to initialize: {e}")
        print(f"✗ TTS Failed: {e}")

    print("\n=== VIRA READY ===")
    
    # 3. Start Execution
    try:
        # Start Lifecycle
        asyncio.create_task(lifecycle.start())
        
        # Start listening for voice (runs as an asyncio task)
        if 'voice' in modules and hasattr(modules['voice'], 'run'):
            asyncio.create_task(modules['voice'].run())
            
        # Keep application running until interrupted
        await asyncio.Event().wait()
        
    except asyncio.CancelledError:
        logger.info("Main execution cancelled (likely shutdown).")
    except Exception as e:
        logger.error(f"Error during VIRA execution: {e}")
    finally:
        # 4. Graceful Shutdown
        print("\nShutting down VIRA...")
        logger.info("Initiating graceful shutdown...")
        
        # Explicitly shutdown TTS background thread if exists
        if 'tts' in modules and hasattr(modules['tts'], 'core'):
            if hasattr(modules['tts'].core, 'shutdown'):
                modules['tts'].core.shutdown()
                
        # Other module shutdown routines can be added here as needed
        
        print("Shutdown complete. Goodbye.")

if __name__ == "__main__":
    try:
        # Avoid 'Event loop closed' warning in Windows when forcefully exiting
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.critical(f"Fatal crash: {e}")
