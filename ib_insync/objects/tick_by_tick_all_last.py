"""TickByTickAllLast NamedTuple."""

from datetime import datetime
from typing import NamedTuple

from .tick_attrib_last import TickAttribLast


class TickByTickAllLast(NamedTuple):
    tickType: int
    time: datetime
    price: float
    size: float
    tickAttribLast: TickAttribLast
    exchange: str
    specialConditions: str
