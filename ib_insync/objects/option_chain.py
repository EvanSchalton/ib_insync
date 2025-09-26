"""OptionChain NamedTuple."""

from typing import NamedTuple


class OptionChain(NamedTuple):
    exchange: str
    underlyingConId: int
    tradingClass: str
    multiplier: str
    expirations: list[str]
    strikes: list[float]
