"""NewsProvider dataclass."""

from dataclasses import dataclass


@dataclass
class NewsProvider:
    code: str = ''
    name: str = ''
