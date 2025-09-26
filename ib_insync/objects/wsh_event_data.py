"""WshEventData dataclass."""

from dataclasses import dataclass

from ..util import UNSET_INTEGER


@dataclass
class WshEventData:
    conId: int = UNSET_INTEGER
    filter: str = ''
    fillWatchlist: bool = False
    fillPortfolio: bool = False
    fillCompetitors: bool = False
    startDate: str = ''
    endDate: str = ''
    totalLimit: int = UNSET_INTEGER
