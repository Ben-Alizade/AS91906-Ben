from dataclasses import dataclass

@dataclass
class ResearchItem:
    title: str
    url: str
    date: str
    authors: str
    summary: str
    tags: set[str]
    trending: bool = False
    saved: bool = False
    read: bool = False