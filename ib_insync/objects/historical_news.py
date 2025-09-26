"""HistoricalNews NamedTuple."""

from datetime import datetime
from typing import NamedTuple


class HistoricalNews(NamedTuple):
    time: datetime
    providerCode: str
    articleId: str
    headline: str
