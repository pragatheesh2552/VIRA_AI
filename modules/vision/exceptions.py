class VisionModuleError(Exception):
    """Base exception for the Vision Engine module."""
    pass

class ScreenshotError(VisionModuleError):
    """Raised when capturing the screen fails."""
    pass

class GeminiVisionError(VisionModuleError):
    """Raised when the Gemini API fails to process the image."""
    pass
