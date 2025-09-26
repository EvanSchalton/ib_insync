"""Reference price types for volatility orders."""

from enum import Enum


class ReferencePriceType(int, Enum):
    """Reference price types for volatility orders."""

    AVERAGE = 1  # Average of bid/ask
    BID_OR_ASK = 2  # Bid when buying, ask when selling
