"""One-Cancels-All (OCA) group types for linked orders."""

from enum import Enum


class OneCancelsAllType(int, Enum):
    """One-Cancels-All (OCA) group types for linked orders."""

    CANCEL_WITH_BLOCK = 1  # Cancel all remaining orders with block
    REDUCE_WITH_BLOCK = 2  # Reduce quantity with block
    REDUCE_WITHOUT_BLOCK = 3  # Reduce quantity without block
