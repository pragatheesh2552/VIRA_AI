from core.event_bus import EventBus
from modules.tts.core import TTSCore
from modules.tts.exceptions import TTSModuleError
from utils.logger import get_logger

logger = get_logger("TTSEngine")

class TTSEngine:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.core = TTSCore()
        
        # Subscribe to relevant completion and failure events
        self.event_bus.subscribe("cognitive_response", self.handle_cognitive)
        
        self.event_bus.subscribe("automation_completed", self.handle_automation_completed)
        self.event_bus.subscribe("automation_failed", self.handle_automation_failed)
        
        self.event_bus.subscribe("browser_completed", self.handle_browser_completed)
        self.event_bus.subscribe("browser_failed", self.handle_browser_failed)
        
        self.event_bus.subscribe("memory_saved", self.handle_memory_saved)
        self.event_bus.subscribe("memory_found", self.handle_memory_found)
        self.event_bus.subscribe("memory_deleted", self.handle_memory_deleted)
        self.event_bus.subscribe("memory_not_found", self.handle_memory_not_found)
        
        self.event_bus.subscribe("assistant_speak", self.handle_assistant_speak)
        
        logger.info("TTSEngine initialized and subscribed to various events.")

    # -- Generic Speak Callback --
    async def handle_assistant_speak(self, payload):
        try:
            text = payload.text if hasattr(payload, 'text') else payload.get("text", "")
            self.core.speak(text)
        except Exception as e:
            logger.error(f"Error handling assistant_speak TTS: {e}")

    # -- Cognitive Callbacks --
    async def handle_cognitive(self, payload):
        try:
            text = payload.response_text if hasattr(payload, 'response_text') else payload.get("response_text", "")
            self.core.speak(text)
        except Exception as e:
            logger.error(f"Error handling cognitive_response TTS: {e}")

    # -- Automation Callbacks --
    async def handle_automation_completed(self, payload):
        try:
            # E.g. "Opened application: calculator"
            action = payload.action_taken if hasattr(payload, 'action_taken') else payload.get("action_taken", "")
            
            # Format nicely for speech (e.g. "Opened application calculator")
            speech = action.replace(":", "") 
            self.core.speak(speech)
        except Exception as e:
            logger.error(f"Error handling automation_completed TTS: {e}")

    async def handle_automation_failed(self, payload):
        try:
            self.core.speak("I could not complete that automation task.")
        except Exception as e:
            logger.error(f"Error handling automation_failed TTS: {e}")

    # -- Browser Callbacks --
    async def handle_browser_completed(self, payload):
        try:
            # E.g. "Opened Youtube" or "Searched Google for 'x'"
            action = payload.action_taken if hasattr(payload, 'action_taken') else payload.get("action_taken", "")
            self.core.speak(action)
        except Exception as e:
            logger.error(f"Error handling browser_completed TTS: {e}")

    async def handle_browser_failed(self, payload):
        try:
            self.core.speak("I couldn't open the browser for that request.")
        except Exception as e:
            logger.error(f"Error handling browser_failed TTS: {e}")

    # -- Memory Callbacks --
    async def handle_memory_saved(self, payload):
        try:
            self.core.speak("I'll remember that.")
        except Exception as e:
            logger.error(f"Error handling memory_saved TTS: {e}")

    async def handle_memory_found(self, payload):
        try:
            results = payload.results if hasattr(payload, 'results') else payload.get("results", [])
            if results:
                # Speak the first result or combine them
                if len(results) == 1:
                    self.core.speak(f"I remember: {results[0]}")
                else:
                    self.core.speak(f"I found {len(results)} memories. The most recent is: {results[0]}")
        except Exception as e:
            logger.error(f"Error handling memory_found TTS: {e}")

    async def handle_memory_deleted(self, payload):
        try:
            count = payload.count if hasattr(payload, 'count') else payload.get("count", 0)
            self.core.speak(f"I have forgotten {count} memories regarding that.")
        except Exception as e:
            logger.error(f"Error handling memory_deleted TTS: {e}")

    async def handle_memory_not_found(self, payload):
        try:
            self.core.speak("I couldn't find any memories about that.")
        except Exception as e:
            logger.error(f"Error handling memory_not_found TTS: {e}")
