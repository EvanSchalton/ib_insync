"""TickByTickMidPoint NamedTuple."""

from datetime import datetime
from typing import NamedTuple


class TickByTickMidPoint(NamedTuple):
    time: datetime
    midPoint: float
