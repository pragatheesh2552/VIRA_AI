from dataclasses import dataclass

@dataclass
class BrowserCompletedPayload:
    original_command: str
    url_opened: str
    action_taken: str

@dataclass
class BrowserFailedPayload:
    original_command: str
    reason: str
