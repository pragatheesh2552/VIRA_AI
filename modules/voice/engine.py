import asyncio
from core.event_bus import EventBus
from core.lifecycle import SystemState
from modules.voice.core import VoiceCore
from modules.voice.models import SpeechPayload
from modules.voice.exceptions import VoiceModuleError
from utils.logger import get_logger

logger = get_logger("VoiceEngine")

class VoiceEngine:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.core = VoiceCore()
        self.is_running = False
        self.is_sleeping = False
        
        # Subscribe to system state changes
        self.event_bus.subscribe("system_state_changed", self.handle_state_change)
        logger.info("VoiceEngine initialized and subscribed to Event Bus.")
        
    async def handle_state_change(self, payload: dict):
        state = payload.get("state")
        if state == SystemState.SLEEPING.value:
            self.is_sleeping = True
            logger.info("VoiceEngine going to sleep mode. Pausing listening.")
        elif state == SystemState.RUNNING.value:
            self.is_sleeping = False
            logger.info("VoiceEngine is active. Resuming listening.")
        elif state == SystemState.SHUTTING_DOWN.value:
            self.is_running = False
            logger.info("VoiceEngine shutting down.")

    async def run(self):
        """Main asynchronous loop for the Voice Engine."""
        self.is_running = True
        logger.info("Voice Engine started its listening loop.")
        
        while self.is_running:
            if self.is_sleeping:
                await asyncio.sleep(1)
                continue
                
            try:
                # Listen continuously for speech using STT
                text = await asyncio.to_thread(self.core.listen_for_speech)
                
                if text:
                    logger.debug(f"Heard raw text: '{text}'")
                    command = self.core.extract_command(text)
                    
                    if command is not None:
                        logger.info(f"Wake word detected! Command: '{command}'")
                        payload = SpeechPayload(text=command, is_wake_word=True)
                        await self.event_bus.publish("speech_recognized", payload)
                    else:
                        logger.debug("Wake word not found in speech. Ignoring.")
                        
            except VoiceModuleError as e:
                logger.error(f"Voice Engine Error: {e}")
                await self.event_bus.publish("system_error", {"source": "voice", "error": str(e)})
                await asyncio.sleep(5) # Backoff on hardware/api error
            except Exception as e:
                logger.error(f"Unexpected error in Voice Engine loop: {e}")
                await asyncio.sleep(1)
