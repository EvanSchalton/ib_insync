"""Contract details and related classes using Pydantic."""

import datetime as dt
from typing import NamedTuple

from pydantic import BaseModel, ConfigDict, Field

from .base import Contract


class TagValue(NamedTuple):
    """Tag-value pair for various IB API uses."""
    tag: str
    value: str


class TradingSession(NamedTuple):
    """Trading session with start and end times."""
    start: dt.datetime
    end: dt.datetime


class ContractDetails(BaseModel):
    """
    Detailed contract information from IB.

    This contains extensive information about a contract including
    trading hours, market rules, and other metadata.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )

    # The contract itself
    contract: Contract | None = None

    # Market data
    market_name: str | None = None
    min_tick: float = 0.0
    order_types: str | None = None
    valid_exchanges: str | None = None
    price_magnifier: int = 0

    # Underlying info
    underlying_contract_id: int = 0
    long_name: str | None = None
    contract_month: str | None = None

    # Categories
    industry: str | None = None
    category: str | None = None
    subcategory: str | None = None

    # Time and trading hours
    time_zone_id: str | None = None
    trading_hours: str | None = None
    liquid_hours: str | None = None

    # Execution rules
    evaluation_rule: str | None = None
    evaluation_multiplier: int = 0
    market_data_size_multiplier: int = 1  # obsolete

    # Aggregation and market rules
    aggregation_group: int = 0
    under_symbol: str | None = None
    underlying_security_type: str | None = None
    market_rule_ids: str | None = None
    security_id_list: list[TagValue] = Field(default_factory=list)

    # Dates
    real_expiration_date: str | None = None
    last_trade_time: str | None = None

    # Stock specific
    stock_type: str | None = None

    # Size limits
    min_size: float = 0.0
    size_increment: float = 0.0
    suggested_size_increment: float = 0.0

    # Bond specific fields
    cusip: str | None = None
    ratings: str | None = None
    description_append: str | None = None
    bond_type: str | None = None
    coupon_type: str | None = None
    callable: bool = False
    putable: bool = False
    coupon: float = 0.0
    convertible: bool = False
    maturity: str | None = None
    issue_date: str | None = None
    next_option_date: str | None = None
    next_option_type: str | None = None
    next_option_partial: bool = False
    notes: str | None = None

    def trading_sessions(self) -> list[TradingSession]:
        """Parse trading hours into TradingSession objects."""
        return self._parse_sessions(self.trading_hours)

    def liquid_sessions(self) -> list[TradingSession]:
        """Parse liquid hours into TradingSession objects."""
        return self._parse_sessions(self.liquid_hours)

    def _parse_sessions(self, s: str | None) -> list[TradingSession]:
        """
        Parse session string into list of TradingSession objects.

        Args:
            s: Session string from IB API

        Returns:
            List of TradingSession objects
        """
        if not s:
            return []

        # Import here to avoid circular dependency
        import ib_insync.util as util

        tz = util.ZoneInfo(self.time_zone_id) if self.time_zone_id else None
        sessions = []

        for sess in s.split(';'):
            if not sess or 'CLOSED' in sess:
                continue
            try:
                start_str, end_str = sess.split('-')
                start = dt.datetime.strptime(start_str, '%Y%m%d:%H%M')
                end = dt.datetime.strptime(end_str, '%Y%m%d:%H%M')

                if tz:
                    start = start.replace(tzinfo=tz)
                    end = end.replace(tzinfo=tz)

                sessions.append(TradingSession(start, end))
            except (ValueError, AttributeError):
                continue

        return sessions


class ContractDescription(BaseModel):
    """
    Brief contract description with derivative types.

    Used in contract searches to describe available contracts.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )

    contract: Contract | None = None
    derivative_security_types: list[str] = Field(default_factory=list)


class ScanData(BaseModel):
    """
    Scanner data for a contract.

    Contains ranking and projection information from market scanners.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )

    rank: int
    contract_details: ContractDetails
    distance: str | None = None
    benchmark: str | None = None
    projection: str | None = None
    legs_str: str | None = None
