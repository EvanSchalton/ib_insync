"""HistoricalTickLast NamedTuple."""

from datetime import datetime
from typing import NamedTuple

from .tick_attrib_last import TickAttribLast


class HistoricalTickLast(NamedTuple):
    time: datetime
    tickAttribLast: TickAttribLast
    price: float
    size: float
    exchange: str
    specialConditions: str
