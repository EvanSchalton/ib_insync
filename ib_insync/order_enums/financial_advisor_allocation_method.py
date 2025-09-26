"""Financial Advisor allocation methods for distributing orders across client accounts."""

from enum import Enum


class FinancialAdvisorAllocationMethod(str, Enum):
    """Financial Advisor allocation methods for distributing orders across client accounts."""

    EQUAL_QUANTITY = "EqualQuantity"  # Distribute shares equally
    NET_LIQUIDATION = "NetLiq"  # Allocate based on net liquidation value
    AVAILABLE_EQUITY = "AvailableEquity"  # Allocate based on available equity
    PCT_CHANGE = "PctChange"  # Maintain percentage ratios
