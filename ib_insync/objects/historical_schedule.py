"""HistoricalSchedule dataclass."""

from dataclasses import dataclass, field

from .historical_session import HistoricalSession


@dataclass
class HistoricalSchedule:
    startDateTime: str = ''
    endDateTime: str = ''
    timeZone: str = ''
    sessions: list[HistoricalSession] = field(default_factory=list)
