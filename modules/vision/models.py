from dataclasses import dataclass

@dataclass
class VisionResponsePayload:
    original_command: str
    response_text: str

@dataclass
class VisionFailedPayload:
    original_command: str
    reason: str
