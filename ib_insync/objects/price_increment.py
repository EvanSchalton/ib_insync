"""PriceIncrement NamedTuple."""

from typing import NamedTuple


class PriceIncrement(NamedTuple):
    lowEdge: float
    increment: float
