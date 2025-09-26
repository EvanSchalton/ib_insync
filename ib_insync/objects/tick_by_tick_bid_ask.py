"""TickByTickBidAsk NamedTuple."""

from datetime import datetime
from typing import NamedTuple

from .tick_attrib_bid_ask import TickAttribBidAsk


class TickByTickBidAsk(NamedTuple):
    time: datetime
    bidPrice: float
    askPrice: float
    bidSize: float
    askSize: float
    tickAttribBidAsk: TickAttribBidAsk
