"""RealTimeBar dataclass."""

from dataclasses import dataclass
from datetime import datetime

from ..util import EPOCH


@dataclass
class RealTimeBar:
    time: datetime = EPOCH
    endTime: int = -1
    open_: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    volume: float = 0.0
    wap: float = 0.0
    count: int = 0
