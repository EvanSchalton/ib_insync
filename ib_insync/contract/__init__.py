"""
Modern Pydantic-based contract system for IB API.

This module provides type-safe, validated contract models using Pydantic
with snake_case naming conventions and proper enum support.
"""

# Base contract and supporting classes
# Contract adapter for polymorphic parsing
from .adapter import (
    ContractAdapter,
    SpecializedContractUnion,
)
from .base import ComboLeg, Contract, DeltaNeutralContract

# Contract details and related classes
from .details import (
    ContractDescription,
    ContractDetails,
    ScanData,
    TagValue,
    TradingSession,
)

# Enumerations
from .enums import (
    Currency,
    Exchange,
    ExemptCode,
    OpenClose,
    OptionType,
    OrderAction,
    SecurityIdType,
    SecurityType,
    ShortSaleSlot,
)

# Specialized contract types
from .specialized import (
    CFD,
    Bag,
    Bond,
    Commodity,
    ContFuture,
    Crypto,
    Forex,
    Future,
    FuturesOption,
    Index,
    MutualFund,
    Option,
    Stock,
    Warrant,
)

# Backward compatibility layer is minimal now
# Use ContractAdapter.parse() directly instead of create_contract()

__all__ = [
    # Base classes
    "Contract",
    "ComboLeg",
    "DeltaNeutralContract",
    # Contract details
    "TagValue",
    "TradingSession",
    "ContractDetails",
    "ContractDescription",
    "ScanData",
    # Enums
    "SecurityType",
    "OptionType",
    "OrderAction",
    "Exchange",
    "Currency",
    "SecurityIdType",
    "OpenClose",
    "ShortSaleSlot",
    "ExemptCode",
    # Specialized contracts
    "Stock",
    "Option",
    "Future",
    "ContFuture",
    "Forex",
    "Index",
    "CFD",
    "Bond",
    "Commodity",
    "FuturesOption",
    "MutualFund",
    "Warrant",
    "Bag",
    "Crypto",
    # Adapters and utilities
    "ContractAdapter",
    "SpecializedContractUnion",
]

# Version info
__version__ = "2.0.0"
