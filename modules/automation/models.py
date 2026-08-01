from dataclasses import dataclass

@dataclass
class AutomationCompletedPayload:
    original_command: str
    action_taken: str

@dataclass
class AutomationFailedPayload:
    original_command: str
    reason: str
