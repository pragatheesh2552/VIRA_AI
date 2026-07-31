class RouterModuleError(Exception):
    """Base exception for the Router module."""
    pass

class ClassificationError(RouterModuleError):
    """Raised when there is a fatal error during command classification."""
    pass
