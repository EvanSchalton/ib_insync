"""TradeLogEntry dataclass."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class TradeLogEntry:
    time: datetime
    status: str = ''
    message: str = ''
    errorCode: int = 0
