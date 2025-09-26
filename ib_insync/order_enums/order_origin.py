"""Order origin type (customer vs firm)."""

from enum import Enum


class OrderOrigin(int, Enum):
    """Order origin type (customer vs firm)."""

    CUSTOMER = 0  # Customer origin
    FIRM = 1  # Firm origin
