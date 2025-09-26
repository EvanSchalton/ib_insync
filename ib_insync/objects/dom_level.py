"""DOMLevel NamedTuple."""

from typing import NamedTuple


class DOMLevel(NamedTuple):
    price: float
    size: float
    marketMaker: str
