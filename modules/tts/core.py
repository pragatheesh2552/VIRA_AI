import threading
import queue
import pyttsx3
import time

from modules.tts.config import TTS_CONFIG
from modules.tts.exceptions import SpeechGenerationError
from utils.logger import get_logger

logger = get_logger("TTSCore")

class TTSCore:
    def __init__(self):
        # We use a thread-safe queue to ensure phrases don't overlap
        self.speech_queue = queue.Queue()
        self._running = True
        
        # Start the background thread
        self.worker_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.worker_thread.start()
        
        logger.info("TTSCore initialized with background worker thread.")

    def _speech_worker(self):
        """
        Background worker that initializes pyttsx3 and loops over the speech queue.
        This ensures pyttsx3's runAndWait() doesn't block the main asyncio Event Bus.
        """
        try:
            # Initialize engine in this specific thread (important for Windows COM)
            engine = pyttsx3.init()
            
            # Apply configuration
            engine.setProperty('rate', TTS_CONFIG.get("rate", 150))
            engine.setProperty('volume', TTS_CONFIG.get("volume", 0.9))
            
            logger.info("pyttsx3 engine initialized successfully.")
            
            while self._running:
                try:
                    # Block until an item is in the queue, timeout 1 second to check self._running
                    text = self.speech_queue.get(timeout=1.0)
                    
                    if text:
                        logger.debug(f"Speaking: {text}")
                        engine.say(text)
                        engine.runAndWait()
                        
                    self.speech_queue.task_done()
                except queue.Empty:
                    continue
                except Exception as e:
                    logger.error(f"Error during speech playback: {e}")
                    
        except Exception as e:
            logger.error(f"Failed to initialize pyttsx3 in background thread: {e}")

    def speak(self, text: str):
        """
        Public method to push a phrase to the speech queue.
        """
        if not text:
            return
            
        try:
            self.speech_queue.put(text)
            logger.debug(f"Queued for speech: '{text}'")
        except Exception as e:
            raise SpeechGenerationError(f"Failed to queue speech: {e}")
            
    def shutdown(self):
        """Gracefully shuts down the background thread."""
        self._running = False
        if self.worker_thread.is_alive():
            self.worker_thread.join(timeout=2.0)
