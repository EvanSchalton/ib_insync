"""OptionComputation NamedTuple."""

from typing import NamedTuple


class OptionComputation(NamedTuple):
    tickAttrib: int
    impliedVol: float | None
    delta: float | None
    optPrice: float | None
    pvDividend: float | None
    gamma: float | None
    vega: float | None
    theta: float | None
    undPrice: float | None
