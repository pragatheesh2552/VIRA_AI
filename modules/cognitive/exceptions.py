class CognitiveModuleError(Exception):
    """Base exception for the Cognitive Engine module."""
    pass

class GeminiAPIError(CognitiveModuleError):
    """Raised when there is an issue communicating with the Gemini API."""
    pass
