class MemoryModuleError(Exception):
    """Base exception for the Memory Engine module."""
    pass

class DatabaseError(MemoryModuleError):
    """Raised when a database operation fails."""
    pass
