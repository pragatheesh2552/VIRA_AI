class BrowserModuleError(Exception):
    """Base exception for the Browser Engine module."""
    pass

class InvalidURLError(BrowserModuleError):
    """Raised when an invalid URL is provided or a search query fails."""
    pass
