from dataclasses import dataclass

@dataclass
class ResearchItem:
    title: str
    url: str
    source: str
    summary: str
    tags: set[str]
    saved: bool = False
    read: bool = False