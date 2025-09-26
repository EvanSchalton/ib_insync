"""Improved base Pydantic contract model with better types."""

from decimal import Decimal
from typing import ClassVar

from pydantic import ConfigDict, Field, field_serializer, field_validator

from ..parseable_model import ParseableModel
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


class ComboLeg(ParseableModel):
    """Combo leg for complex orders."""

    model_config = ConfigDict(
        validate_assignment=True,
    )

    # Define parsing order for IB protocol
    _parser_fields: ClassVar[tuple[str, ...]] = (
        'contract_id',
        'ratio',
        'action',
        'exchange',
        'open_close',
        'short_sale_slot',
        'designated_location',
        'exempt_code',
    )

    contract_id: int = 0
    ratio: int | None = None
    action: OrderAction = OrderAction.BUY
    exchange: Exchange | None = None
    open_close: OpenClose = OpenClose.SAME
    short_sale_slot: ShortSaleSlot = ShortSaleSlot.DEFAULT
    designated_location: str | None = None
    exempt_code: ExemptCode = ExemptCode.APPLIES_UPTICK_RULE


class DeltaNeutralContract(ParseableModel):
    """Delta neutral contract for hedging."""

    model_config = ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True,  # For Decimal
    )

    # Define parsing order for IB protocol
    _parser_fields: ClassVar[tuple[str, ...]] = (
        'contract_id',
        'delta',
        'price',
    )

    contract_id: int = 0
    delta: Decimal | None = None
    price: Decimal | None = None

    @field_serializer("delta", "price", when_used="json")
    def serialize_decimal(self, v: Decimal | None) -> str | None:
        """Serialize Decimal to string for JSON."""
        if v is None:
            return None
        return str(v)


class Contract(ParseableModel):
    """
    Base contract class using Pydantic with improved types.

    Key improvements:
    - Decimal for financial amounts (strike, price, etc.)
    - Enums for exchange and currency
    - Integer for multiplier
    - OptionType instead of Right
    - Clear field names (security_id instead of sec_id)
    """

    model_config = ConfigDict(
        validate_assignment=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,  # For Decimal
    )

    # Define parsing order for IB protocol (types handled by Pydantic)
    _parser_fields: ClassVar[tuple[str, ...]] = (
        'contract_id',
        'symbol',
        'security_type',
        'last_trade_date_or_contract_month',
        'strike',
        'option_type',
        'multiplier',
        'exchange',
        'currency',
        'local_symbol',
        'trading_class',
    )

    # Primary identifiers
    contract_id: int = 0
    symbol: str | None = None
    security_type: SecurityType | None = None

    # Contract specifications
    last_trade_date_or_contract_month: str | None = None
    strike: Decimal = Decimal("0")
    option_type: OptionType | None = None  # Renamed from 'right'
    multiplier: str | None = None  # Per IB docs, multiplier is a string

    # Exchange and currency - now using enums
    exchange: Exchange | str | None = None  # Allow str for flexibility
    primary_exchange: Exchange | str | None = None
    currency: Currency | str | None = None

    # Additional identifiers
    local_symbol: str | None = None
    trading_class: str | None = None

    # Configuration flags
    include_expired: bool = False

    # Security identifiers
    security_id_type: SecurityIdType | None = None
    security_id: str | None = None

    # Additional fields
    description: str | None = None
    issuer_id: str | None = None

    # Combo contracts
    combo_legs_description: str | None = None
    combo_legs: list[ComboLeg] = Field(default_factory=list)
    delta_neutral_contract: DeltaNeutralContract | None = None

    # Note: Pydantic automatically handles type conversions for enums, Decimal, and int.
    # We removed all unnecessary validators that were duplicating Pydantic's built-in functionality.
    # If special handling is needed for IB API quirks (like empty strings), it should be done
    # in the parsing layer, not in validators.

    @field_validator("option_type", mode="before")
    @classmethod
    def validate_option_type(cls, v):
        """Convert empty string to None for option_type."""
        if v == "":
            return None
        return v

    # Serializers for Decimal
    @field_serializer("strike", when_used="json")
    def serialize_strike(self, v: Decimal) -> str:
        """Serialize Decimal to string for JSON."""
        if v is None:
            return None
        return str(v)

    def is_hashable(self) -> bool:
        """Check if this contract can be hashed by contract_id."""
        return self.contract_id > 0

    def __hash__(self) -> int:
        """Hash by contract_id if available, otherwise use ParseableModel's auto-hash."""
        if self.is_hashable():
            return hash(self.contract_id)
        # Fall back to ParseableModel's auto-hash based on _parser_fields
        return super().__hash__()

    def __eq__(self, other) -> bool:
        """Contracts are equal if they have the same hash."""
        if not isinstance(other, Contract):
            return False
        # If both have contract_ids, compare just those
        if self.is_hashable() and other.is_hashable():
            return self.contract_id == other.contract_id
        # Otherwise use ParseableModel's equality
        return super().__eq__(other)

    def __repr__(self) -> str:
        """String representation of the contract."""
        attrs = []
        if self.symbol:
            attrs.append(f"symbol='{self.symbol}'")
        if self.security_type:
            attrs.append(f"security_type='{self.security_type}'")
        if self.exchange:
            attrs.append(f"exchange='{self.exchange}'")
        if self.currency:
            attrs.append(f"currency='{self.currency}'")
        if self.strike and self.strike != Decimal("0"):
            attrs.append(f"strike={self.strike}")
        if self.option_type:
            attrs.append(f"option_type='{self.option_type}'")
        return f"Contract({', '.join(attrs)})"
