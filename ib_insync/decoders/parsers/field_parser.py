"""Field parsing utilities for IB protocol messages."""

from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from ib_insync.contract import (
        ComboLeg,
        Contract,
        ContractDetails,
        DeltaNeutralContract,
        TagValue,
    )
    from ib_insync.order import Order, OrderState
from ib_insync.util import parseIBDatetime


class FieldIterator:
    """
    Iterator for consuming fields from IB messages.

    This provides a convenient way to consume fields in order
    while keeping track of position for error reporting.
    """

    def __init__(self, fields: list[str], start_index: int = 0):
        self.fields = fields
        self.index = start_index
        self.length = len(fields)

    def next(self, default: Any = '', empty_to_none: bool = False) -> str | None:
        """
        Get the next field or return default if exhausted.

        Args:
            default: Value to return if no more fields
            empty_to_none: If True, convert empty strings to None

        Returns:
            The next field value, potentially converted to None if empty
        """
        if self.index < self.length:
            value = self.fields[self.index]
            self.index += 1
            if empty_to_none and value == '':
                return None
            return value
        return default

    def next_int(self, default: int = 0) -> int:
        """Get the next field as an integer."""
        value = self.next()
        if value == '':
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def next_float(self, default: float = 0.0) -> float:
        """Get the next field as a float."""
        value = self.next()
        if value == '':
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    def next_bool(self, default: bool = False) -> bool:
        """Get the next field as a boolean."""
        value = self.next()
        if value == '':
            return default
        return value == '1' or value.lower() == 'true'

    def next_datetime(self, default: datetime | None = None) -> datetime | None:
        """Get the next field as a datetime."""
        value = self.next()
        if value == '':
            return default
        try:
            return parseIBDatetime(value)
        except Exception:
            return default

    def peek(self, offset: int = 0) -> str | None:
        """Peek at a field without consuming it."""
        index = self.index + offset
        if index < self.length:
            return self.fields[index]
        return None

    def skip(self, count: int = 1) -> None:
        """Skip the specified number of fields."""
        self.index = min(self.index + count, self.length)

    def has_more(self) -> bool:
        """Check if there are more fields to consume."""
        return self.index < self.length

    def remaining(self) -> int:
        """Get the number of remaining fields."""
        return max(0, self.length - self.index)

    def consume_rest(self) -> list[str]:
        """Consume and return all remaining fields."""
        result = self.fields[self.index:]
        self.index = self.length
        return result


class FieldParser:
    """Utilities for parsing complex IB data structures from fields."""

    @staticmethod
    def parse_contract(fields: FieldIterator) -> 'Contract':
        """
        Parse a Contract from fields using the model's own parsing logic.

        Args:
            fields: Field iterator positioned at the start of contract data

        Returns:
            Parsed Contract object
        """
        from ib_insync.contract import Contract
        return Contract.parse(fields)

    @staticmethod
    def parse_contract_details(fields: FieldIterator, server_version: int = 0) -> 'ContractDetails':
        """
        Parse ContractDetails from fields.

        Args:
            fields: Field iterator
            server_version: Server version for compatibility

        Returns:
            Parsed ContractDetails object
        """
        from ib_insync.contract import ContractDetails, TagValue

        details = ContractDetails()
        details.contract = FieldParser.parse_contract(fields)

        details.marketName = fields.next()
        details.minTick = fields.next_float()
        details.orderTypes = fields.next()
        details.validExchanges = fields.next()
        details.priceMagnifier = fields.next_int()
        details.underConId = fields.next_int()
        details.longName = fields.next()
        details.contractMonth = fields.next()
        details.industry = fields.next()
        details.category = fields.next()
        details.subcategory = fields.next()
        details.timeZoneId = fields.next()
        details.tradingHours = fields.next()
        details.liquidHours = fields.next()
        details.evRule = fields.next()
        details.evMultiplier = fields.next_int()

        # Parse security ID list
        num_sec_ids = fields.next_int()
        if num_sec_ids > 0:
            details.secIdList = []
            for _ in range(num_sec_ids):
                tag = fields.next()
                value = fields.next()
                details.secIdList.append(TagValue(tag, value))

        details.aggGroup = fields.next_int()
        details.underSymbol = fields.next()
        details.underSecType = fields.next()
        details.marketRuleIds = fields.next()
        details.realExpirationDate = fields.next()
        details.stockType = fields.next()

        # Version-specific fields
        if server_version >= 164:
            details.minSize = fields.next_float()
            details.sizeIncrement = fields.next_float()
            details.suggestedSizeIncrement = fields.next_float()

        return details

    @staticmethod
    def parse_order(fields: FieldIterator, server_version: int = 0) -> 'Order':
        """
        Parse an Order from fields.

        Args:
            fields: Field iterator
            server_version: Server version for compatibility

        Returns:
            Parsed Order object
        """
        order = Order()

        # Basic order fields
        order.orderId = fields.next_int()
        order.clientId = fields.next_int()
        order.permId = fields.next_int()
        order.action = fields.next()
        order.totalQuantity = fields.next_float()
        order.orderType = fields.next()
        order.lmtPrice = fields.next_float()
        order.auxPrice = fields.next_float()
        order.tif = fields.next()
        order.ocaGroup = fields.next()
        order.ocaType = fields.next_int()
        order.orderRef = fields.next()
        order.transmit = fields.next_bool()
        order.parentId = fields.next_int()
        order.blockOrder = fields.next_bool()
        order.sweepToFill = fields.next_bool()
        order.displaySize = fields.next_int()
        order.triggerMethod = fields.next_int()
        order.outsideRth = fields.next_bool()
        order.hidden = fields.next_bool()

        # Extended fields (simplified - full implementation would handle all fields)
        order.goodAfterTime = fields.next()
        order.goodTillDate = fields.next()
        order.rule80A = fields.next()
        order.allOrNone = fields.next_bool()
        order.minQty = fields.next_int()
        order.percentOffset = fields.next_float()

        return order

    @staticmethod
    def parse_order_state(fields: FieldIterator) -> 'OrderState':
        """
        Parse an OrderState from fields.

        Args:
            fields: Field iterator

        Returns:
            Parsed OrderState object
        """
        state = OrderState()

        state.status = fields.next()
        state.initMarginBefore = fields.next()
        state.maintMarginBefore = fields.next()
        state.equityWithLoanBefore = fields.next()
        state.initMarginChange = fields.next()
        state.maintMarginChange = fields.next()
        state.equityWithLoanChange = fields.next()
        state.initMarginAfter = fields.next()
        state.maintMarginAfter = fields.next()
        state.equityWithLoanAfter = fields.next()
        state.commission = fields.next_float()
        state.minCommission = fields.next_float()
        state.maxCommission = fields.next_float()
        state.commissionCurrency = fields.next()
        state.warningText = fields.next()
        state.completedTime = fields.next()
        state.completedStatus = fields.next()

        return state

    @staticmethod
    def parse_combo_legs(fields: FieldIterator, count: int) -> list['ComboLeg']:
        """
        Parse multiple ComboLeg objects from fields using model parsing.

        Args:
            fields: Field iterator
            count: Number of combo legs to parse

        Returns:
            List of parsed ComboLeg objects
        """
        from ib_insync.contract import ComboLeg
        return ComboLeg.parse_multiple(fields, count)

    @staticmethod
    def parse_delta_neutral_contract(fields: FieldIterator) -> Optional['DeltaNeutralContract']:
        """
        Parse a DeltaNeutralContract from fields if present.

        Args:
            fields: Field iterator

        Returns:
            Parsed DeltaNeutralContract or None
        """
        has_delta_neutral = fields.next_bool()
        if not has_delta_neutral:
            return None

        from ib_insync.contract import DeltaNeutralContract
        return DeltaNeutralContract.parse(fields)

    @staticmethod
    def parse_tag_values(fields: FieldIterator, count: int) -> list['TagValue']:
        """
        Parse multiple TagValue pairs from fields.

        Args:
            fields: Field iterator
            count: Number of tag values to parse

        Returns:
            List of parsed TagValue objects
        """
        from ib_insync.contract import TagValue

        tag_values = []
        for _ in range(count):
            tag = fields.next()
            value = fields.next()
            tag_values.append(TagValue(tag, value))
        return tag_values
