"""TickData NamedTuple."""

from datetime import datetime
from typing import NamedTuple


class TickData(NamedTuple):
    time: datetime
    tickType: int
    price: float
    size: float
