import speech_recognition as sr
from modules.voice.exceptions import MicrophoneError, SpeechRecognitionError
from modules.voice.config import WAKE_WORD, TIMEOUT, PHRASE_TIME_LIMIT, ENERGY_THRESHOLD, DEVICE_INDEX
from utils.logger import get_logger

logger = get_logger("VoiceCore")

class VoiceCore:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = ENERGY_THRESHOLD
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.non_speaking_duration = 0.6
        
        try:
            self.microphone = sr.Microphone(device_index=DEVICE_INDEX)
        except AttributeError as e:
            raise MicrophoneError(f"PyAudio might not be installed. Failed to get microphone: {e}")
        
        # Adjust for ambient noise on init
        try:
            with self.microphone as source:
                logger.info("Adjusting for ambient noise. Please wait...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Ambient noise adjustment complete.")
        except Exception as e:
            raise MicrophoneError(f"Failed to initialize microphone: {e}")

    def listen_for_speech(self, phrase_time_limit: int = PHRASE_TIME_LIMIT) -> str:
        """
        Listens to the microphone and returns the transcribed text.
        Blocks until speech is heard or timeout.
        """
        try:
            with self.microphone as source:
                logger.info("Listening...")
                audio = self.recognizer.listen(source, timeout=TIMEOUT, phrase_time_limit=phrase_time_limit)
                
            text = self.recognizer.recognize_google(audio, language="en-IN")
            logger.debug(f"Recognized text (en-IN): '{text}'")
            return text.lower()
            
        except sr.WaitTimeoutError:
            return "" # No speech detected within timeout
        except sr.UnknownValueError:
            return "" # Speech was unintelligible
        except sr.RequestError as e:
            raise SpeechRecognitionError(f"Could not request results from STT service; {e}")
        except Exception as e:
            raise MicrophoneError(f"An unexpected microphone error occurred: {e}")

    def extract_command(self, text: str) -> str | None:
        """
        Checks if the recognized text starts with the wake word (or common variations).
        If it does, returns the command by stripping the wake word.
        If it doesn't, returns None.
        """
        if not text:
            return None
            
        # Common STT misspellings for 'Vira'
        variations = [WAKE_WORD, "veera", "vera", "mira", "era", "we're a", "here a"]
        text_lower = text.lower().strip()
        
        for variant in variations:
            if text_lower.startswith(variant):
                # Strip the wake word
                command = text_lower[len(variant):].strip()
                # Strip leading punctuation if STT added any (e.g., "Vira, what...")
                if command.startswith(",") or command.startswith(".") or command.startswith("-"):
                    command = command[1:].strip()
                return command
                
        return None
