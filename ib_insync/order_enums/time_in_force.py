"""Time in Force values for orders."""

from enum import Enum


class TimeInForce(str, Enum):
    """Time in Force values for orders."""

    DAY = "DAY"
    GOOD_TILL_CANCELLED = "GTC"
    IMMEDIATE_OR_CANCEL = "IOC"
    GOOD_TILL_DATE = "GTD"
    AT_THE_OPENING = "OPG"
    FILL_OR_KILL = "FOK"
    DAY_TILL_CANCELLED = "DTC"
