from dataclasses import dataclass

@dataclass
class RoutedCommandPayload:
    original_text: str
    category: str
