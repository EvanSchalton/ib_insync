"""HistoricalTickBidAsk NamedTuple."""

from datetime import datetime
from typing import NamedTuple

from .tick_attrib_bid_ask import TickAttribBidAsk


class HistoricalTickBidAsk(NamedTuple):
    time: datetime
    tickAttribBidAsk: TickAttribBidAsk
    priceBid: float
    priceAsk: float
    sizeBid: float
    sizeAsk: float
