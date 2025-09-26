"""Improved specialized contract types with better typing."""

from decimal import Decimal
from typing import Literal

from pydantic import Field, field_validator, model_validator

from .base import Contract
from .enums import Currency, Exchange, OptionType, SecurityType


class Stock(Contract):
    """Stock contract - automatically sets security_type to STOCK."""

    security_type: Literal[SecurityType.STOCK] = SecurityType.STOCK
    exchange: Exchange = Exchange.SMART
    currency: Currency = Currency.USD


class Option(Contract):
    """Option contract - automatically sets security_type to OPTION."""

    security_type: Literal[SecurityType.OPTION] = SecurityType.OPTION

    # Required fields for options
    strike: Decimal = Field(..., gt=0, description="Strike price")
    option_type: OptionType = Field(..., description="CALL or PUT")

    # Common defaults
    multiplier: int = 100
    exchange: Exchange = Exchange.SMART
    currency: Currency = Currency.USD

    @field_validator("option_type")
    @classmethod
    def validate_option_type_required(cls, v):
        """Ensure option type is specified."""
        if v is None:
            raise ValueError("Option type (CALL/PUT) is required")
        return v


class Future(Contract):
    """Futures contract - automatically sets security_type to FUTURE."""

    security_type: Literal[SecurityType.FUTURE] = SecurityType.FUTURE
    currency: Currency = Currency.USD

    # Futures typically require exchange to be specified
    exchange: Exchange = Field(..., description="Exchange is required for futures")


class ContFuture(Contract):
    """Continuous future - automatically sets security_type to CONTINUOUS_FUTURE."""

    security_type: Literal[SecurityType.CONTINUOUS_FUTURE] = SecurityType.CONTINUOUS_FUTURE
    currency: Currency = Currency.USD


class Forex(Contract):
    """Foreign exchange contract - automatically sets security_type to FOREX."""

    security_type: Literal[SecurityType.FOREX] = SecurityType.FOREX
    exchange: Exchange = Exchange.IDEALPRO

    @model_validator(mode="before")
    @classmethod
    def handle_pair(cls, values):
        """Handle the pair shortcut (e.g., EURUSD -> EUR + USD)."""
        if isinstance(values, dict):
            pair = values.get("pair")
            if pair and len(pair) == 6:
                # Set symbol and currency from pair if not already set
                if "symbol" not in values or values["symbol"] is None:
                    values["symbol"] = pair[:3]
                if "currency" not in values or values["currency"] is None:
                    values["currency"] = pair[3:]
        return values

    def pair(self) -> str:
        """Get the currency pair string (e.g., 'EURUSD')."""
        if self.symbol and self.currency:
            # Handle both enum and string
            symbol_str = self.symbol if isinstance(self.symbol, str) else self.symbol.value
            currency_str = self.currency.value if hasattr(self.currency, 'value') else str(self.currency)
            return f"{symbol_str}{currency_str}"
        return ""


class Index(Contract):
    """Index contract - automatically sets security_type to INDEX."""

    security_type: Literal[SecurityType.INDEX] = SecurityType.INDEX
    currency: Currency = Currency.USD


class CFD(Contract):
    """Contract for Difference - automatically sets security_type to CFD."""

    security_type: Literal[SecurityType.CFD] = SecurityType.CFD


class Commodity(Contract):
    """Commodity contract - automatically sets security_type to COMMODITY."""

    security_type: Literal[SecurityType.COMMODITY] = SecurityType.COMMODITY


class Bond(Contract):
    """Bond contract - automatically sets security_type to BOND."""

    security_type: Literal[SecurityType.BOND] = SecurityType.BOND

    # Bonds often use security IDs for identification
    # security_id_type and security_id should be provided


class FuturesOption(Contract):
    """Futures option - automatically sets security_type to FUTURES_OPTION."""

    security_type: Literal[SecurityType.FUTURES_OPTION] = SecurityType.FUTURES_OPTION

    # Required fields
    strike: Decimal = Field(..., gt=0, description="Strike price")
    option_type: OptionType = Field(..., description="CALL or PUT")

    # Defaults
    currency: Currency = Currency.USD


class MutualFund(Contract):
    """Mutual fund - automatically sets security_type to FUND."""

    security_type: Literal[SecurityType.FUND] = SecurityType.FUND


class Warrant(Contract):
    """Warrant - automatically sets security_type to WARRANT."""

    security_type: Literal[SecurityType.WARRANT] = SecurityType.WARRANT


class Bag(Contract):
    """Combo/Bag contract - automatically sets security_type to COMBO."""

    security_type: Literal[SecurityType.COMBO] = SecurityType.COMBO

    @model_validator(mode="after")
    def validate_combo_legs(self):
        """Ensure combo legs are specified."""
        if not self.combo_legs:
            raise ValueError("Bag contracts must have combo_legs defined")
        return self


class Crypto(Contract):
    """Cryptocurrency contract - automatically sets security_type to CRYPTO."""

    security_type: Literal[SecurityType.CRYPTO] = SecurityType.CRYPTO
    exchange: Exchange = Exchange.PAXOS
    currency: Currency = Currency.USD
