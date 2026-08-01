from dataclasses import dataclass
from typing import List

@dataclass
class MemorySavedPayload:
    content: str

@dataclass
class MemoryFoundPayload:
    query: str
    results: List[str]

@dataclass
class MemoryDeletedPayload:
    query: str
    count: int

@dataclass
class MemoryNotFoundPayload:
    query: str
