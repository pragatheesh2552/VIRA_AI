class AutomationModuleError(Exception):
    """Base exception for the Automation Engine module."""
    pass

class ActionFailedError(AutomationModuleError):
    """Raised when an automation action fails (e.g., app not found)."""
    pass
