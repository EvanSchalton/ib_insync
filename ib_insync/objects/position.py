"""Position NamedTuple."""

from typing import NamedTuple

from ..contract import Contract


class Position(NamedTuple):
    account: str
    contract: Contract
    position: float
    avgCost: float
