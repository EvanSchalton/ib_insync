"""BOX auction strategy types."""

from enum import Enum


class AuctionStrategy(int, Enum):
    """BOX auction strategy types."""

    MATCH = 1  # Match the auction price
    IMPROVEMENT = 2  # Improve the auction price
    TRANSPARENT = 3  # Transparent auction
