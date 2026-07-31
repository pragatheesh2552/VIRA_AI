class VoiceModuleError(Exception):
    """Base exception for the voice module"""
    pass

class MicrophoneError(VoiceModuleError):
    """Raised when there is an issue accessing the microphone"""
    pass

class SpeechRecognitionError(VoiceModuleError):
    """Raised when the STT engine fails or loses connection"""
    pass
