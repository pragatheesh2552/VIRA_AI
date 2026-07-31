from dataclasses import dataclass

@dataclass
class SpeechPayload:
    text: str
    is_wake_word: bool
    confidence: float = 1.0
