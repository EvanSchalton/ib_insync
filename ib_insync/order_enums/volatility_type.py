"""Volatility types for volatility orders."""

from enum import Enum


class VolatilityType(int, Enum):
    """Volatility types for volatility orders."""

    DAILY = 1  # Daily volatility
    ANNUAL = 2  # Annual volatility
