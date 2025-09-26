"""BarData dataclass."""

from dataclasses import dataclass
from datetime import date as date_
from datetime import datetime

from ..util import EPOCH


@dataclass
class BarData:
    date: date_ | datetime = EPOCH
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    volume: float = 0
    average: float = 0.0
    barCount: int = 0
