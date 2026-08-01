from dataclasses import dataclass

@dataclass
class CognitiveResponsePayload:
    original_prompt: str
    response_text: str
