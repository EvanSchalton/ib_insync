"""Trigger methods for stop orders."""

from enum import Enum


class TriggerMethod(int, Enum):
    """Trigger methods for stop orders."""

    DEFAULT = 0  # Default method
    DOUBLE_BID_ASK = 1  # Double bid/ask method
    LAST = 2  # Last price
    DOUBLE_LAST = 3  # Double last price
    BID_ASK = 4  # Bid/Ask method
    LAST_OR_BID_ASK = 7  # Last or bid/ask
    MIDPOINT = 8  # Midpoint
