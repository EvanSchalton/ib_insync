"""TickAttribBidAsk dataclass."""

from dataclasses import dataclass


@dataclass
class TickAttribBidAsk:
    bidPastLow: bool = False
    askPastHigh: bool = False
