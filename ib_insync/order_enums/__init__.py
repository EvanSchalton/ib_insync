"""
Order-related enumerations for Interactive Brokers API.

This module provides type-safe enums for all order-related constants used
in the Interactive Brokers API, with clear, descriptive names.
"""

from .auction_strategy import AuctionStrategy
from .financial_advisor_allocation_method import FinancialAdvisorAllocationMethod
from .hedge_type import HedgeType
from .one_cancels_all_type import OneCancelsAllType
from .order_origin import OrderOrigin
from .order_type import OrderType
from .reference_price_type import ReferencePriceType
from .time_in_force import TimeInForce
from .trigger_method import TriggerMethod
from .user_type import UserType
from .volatility_type import VolatilityType

__all__ = [
    "AuctionStrategy",
    "FinancialAdvisorAllocationMethod",
    "HedgeType",
    "OneCancelsAllType",
    "OrderOrigin",
    "OrderType",
    "ReferencePriceType",
    "TimeInForce",
    "TriggerMethod",
    "UserType",
    "VolatilityType",
]
