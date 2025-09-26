"""HistoricalTick NamedTuple."""

from datetime import datetime
from typing import NamedTuple


class HistoricalTick(NamedTuple):
    time: datetime
    price: float
    size: float
