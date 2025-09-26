"""HistoricalSession dataclass."""

from dataclasses import dataclass


@dataclass
class HistoricalSession:
    startDateTime: str = ''
    endDateTime: str = ''
    refDate: str = ''
