class TTSModuleError(Exception):
    """Base exception for the TTS Engine module."""
    pass

class SpeechGenerationError(TTSModuleError):
    """Raised when speech synthesis fails."""
    pass
