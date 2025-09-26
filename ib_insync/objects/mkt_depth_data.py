"""MktDepthData NamedTuple."""

from datetime import datetime
from typing import NamedTuple


class MktDepthData(NamedTuple):
    time: datetime
    position: int
    marketMaker: str
    operation: int
    side: int
    price: float
    size: float
