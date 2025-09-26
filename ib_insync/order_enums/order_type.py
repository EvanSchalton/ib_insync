"""Order types supported by Interactive Brokers."""

from enum import Enum


class OrderType(str, Enum):
    """Order types supported by Interactive Brokers."""

    # Basic order types
    MARKET = "MKT"
    LIMIT = "LMT"
    STOP = "STP"
    STOP_LIMIT = "STP LMT"

    # Trailing orders
    TRAILING_STOP = "TRAIL"
    TRAILING_STOP_LIMIT = "TRAIL LIMIT"

    # Relative orders
    RELATIVE = "REL"

    # Pegged orders
    PEGGED_TO_MARKET = "PEG MKT"
    PEGGED_TO_MIDPOINT = "PEG MID"
    PEGGED_TO_PRIMARY = "PEG PRI"

    # Time-based orders
    MARKET_ON_CLOSE = "MOC"
    LIMIT_ON_CLOSE = "LOC"
    MARKET_ON_OPEN = "MOO"
    LIMIT_ON_OPEN = "LOO"

    # Volatility orders
    VOLATILITY = "VOL"
    VOLUME_WEIGHTED_AVERAGE_PRICE = "VWAP"

    # Other order types
    MARKET_IF_TOUCHED = "MIT"
    LIMIT_IF_TOUCHED = "LIT"
    ICEBERG = "ICE"
    BOX_TOP = "BOX"
