"""Hedge types for orders."""

from enum import Enum


class HedgeType(str, Enum):
    """Hedge types for orders."""

    NONE = ""  # No hedge
    DELTA = "D"  # Delta hedge
    BETA = "B"  # Beta hedge
    FX = "F"  # FX hedge
    PAIR = "P"  # Pair hedge
