"""Pydantic models for account-related messages."""

from typing import ClassVar

from pydantic import Field

from ib_insync.contract import Contract
from ib_insync.decoders.base import IBMessage, registry
from ib_insync.decoders.parsers.field_parser import FieldIterator


@registry.register_message(msg_id=6)
class UpdateAccountValueMessage(IBMessage):
    """Update account value message (msg_id=6)."""

    MESSAGE_ID: ClassVar[int] = 6

    key: str
    value: str
    currency: str
    account_name: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'UpdateAccountValueMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(
            key=it.next(),
            value=it.next(),
            currency=it.next(),
            account_name=it.next()
        )


@registry.register_message(msg_id=7)
class UpdatePortfolioMessage(IBMessage):
    """Update portfolio message (msg_id=7)."""

    MESSAGE_ID: ClassVar[int] = 7

    contract: Contract = Field(default_factory=Contract)
    position: float
    market_price: float
    market_value: float
    average_cost: float
    unrealized_pnl: float
    realized_pnl: float
    account_name: str

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'UpdatePortfolioMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        contract = Contract()
        contract.conId = it.next_int()
        contract.symbol = it.next()
        contract.secType = it.next()
        contract.lastTradeDateOrContractMonth = it.next()
        contract.strike = it.next_float()
        contract.right = it.next()
        contract.multiplier = it.next()
        contract.primaryExchange = it.next()
        contract.currency = it.next()
        contract.localSymbol = it.next()
        contract.tradingClass = it.next()

        position = it.next_float()
        market_price = it.next_float()
        market_value = it.next_float()
        average_cost = it.next_float()
        unrealized_pnl = it.next_float()
        realized_pnl = it.next_float()
        account_name = it.next()

        return cls(
            contract=contract,
            position=position,
            market_price=market_price,
            market_value=market_value,
            average_cost=average_cost,
            unrealized_pnl=unrealized_pnl,
            realized_pnl=realized_pnl,
            account_name=account_name
        )


@registry.register_message(msg_id=8)
class UpdateAccountTimeMessage(IBMessage):
    """Update account time message (msg_id=8)."""

    MESSAGE_ID: ClassVar[int] = 8

    time_stamp: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'UpdateAccountTimeMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(time_stamp=it.next())


@registry.register_message(msg_id=54)
class AccountDownloadEndMessage(IBMessage):
    """Account download end message (msg_id=54)."""

    MESSAGE_ID: ClassVar[int] = 54

    account_name: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'AccountDownloadEndMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(account_name=it.next())


@registry.register_message(msg_id=61)
class PositionMessage(IBMessage):
    """Position message (msg_id=61)."""

    MESSAGE_ID: ClassVar[int] = 61

    account: str
    contract: Contract = Field(default_factory=Contract)
    position: float
    avg_cost: float

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'PositionMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        account = it.next()
        contract = Contract()
        contract.conId = it.next_int()
        contract.symbol = it.next()
        contract.secType = it.next()
        contract.lastTradeDateOrContractMonth = it.next()
        contract.strike = it.next_float()
        contract.right = it.next()
        contract.multiplier = it.next()
        contract.exchange = it.next()
        contract.currency = it.next()
        contract.localSymbol = it.next()
        contract.tradingClass = it.next()

        position = it.next_float()
        avg_cost = it.next_float()

        return cls(
            account=account,
            contract=contract,
            position=position,
            avg_cost=avg_cost
        )


@registry.register_message(msg_id=62)
class PositionEndMessage(IBMessage):
    """Position end message (msg_id=62)."""

    MESSAGE_ID: ClassVar[int] = 62

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'PositionEndMessage':
        """Parse from IB wire format fields."""
        return cls()


@registry.register_message(msg_id=63)
class AccountSummaryMessage(IBMessage):
    """Account summary message (msg_id=63)."""

    MESSAGE_ID: ClassVar[int] = 63

    req_id: int
    account: str
    tag: str
    value: str
    currency: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'AccountSummaryMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(
            req_id=it.next_int(),
            account=it.next(),
            tag=it.next(),
            value=it.next(),
            currency=it.next()
        )


@registry.register_message(msg_id=64)
class AccountSummaryEndMessage(IBMessage):
    """Account summary end message (msg_id=64)."""

    MESSAGE_ID: ClassVar[int] = 64

    req_id: int

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'AccountSummaryEndMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(req_id=it.next_int())


@registry.register_message(msg_id=71)
class PositionMultiMessage(IBMessage):
    """Position multi message (msg_id=71)."""

    MESSAGE_ID: ClassVar[int] = 71

    req_id: int
    account: str
    contract: Contract = Field(default_factory=Contract)
    position: float
    avg_cost: float
    model_code: str

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'PositionMultiMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        req_id = it.next_int()
        account = it.next()
        contract = Contract()
        contract.conId = it.next_int()
        contract.symbol = it.next()
        contract.secType = it.next()
        contract.lastTradeDateOrContractMonth = it.next()
        contract.strike = it.next_float()
        contract.right = it.next()
        contract.multiplier = it.next()
        contract.exchange = it.next()
        contract.currency = it.next()
        contract.localSymbol = it.next()
        contract.tradingClass = it.next()

        position = it.next_float()
        avg_cost = it.next_float()
        model_code = it.next()

        return cls(
            req_id=req_id,
            account=account,
            contract=contract,
            position=position,
            avg_cost=avg_cost,
            model_code=model_code
        )


@registry.register_message(msg_id=72)
class PositionMultiEndMessage(IBMessage):
    """Position multi end message (msg_id=72)."""

    MESSAGE_ID: ClassVar[int] = 72

    req_id: int

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'PositionMultiEndMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(req_id=it.next_int())


@registry.register_message(msg_id=73)
class AccountUpdateMultiMessage(IBMessage):
    """Account update multi message (msg_id=73)."""

    MESSAGE_ID: ClassVar[int] = 73

    req_id: int
    account: str
    model_code: str
    key: str
    value: str
    currency: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'AccountUpdateMultiMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(
            req_id=it.next_int(),
            account=it.next(),
            model_code=it.next(),
            key=it.next(),
            value=it.next(),
            currency=it.next()
        )


@registry.register_message(msg_id=74)
class AccountUpdateMultiEndMessage(IBMessage):
    """Account update multi end message (msg_id=74)."""

    MESSAGE_ID: ClassVar[int] = 74

    req_id: int

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'AccountUpdateMultiEndMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(req_id=it.next_int())


@registry.register_message(msg_id=94)
class PnlMessage(IBMessage):
    """PnL message (msg_id=94)."""

    MESSAGE_ID: ClassVar[int] = 94

    req_id: int
    daily_pnl: float
    unrealized_pnl: float
    realized_pnl: float

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'PnlMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        return cls(
            req_id=it.next_int(),
            daily_pnl=it.next_float(),
            unrealized_pnl=it.next_float(),
            realized_pnl=it.next_float()
        )


@registry.register_message(msg_id=95)
class PnlSingleMessage(IBMessage):
    """PnL single message (msg_id=95)."""

    MESSAGE_ID: ClassVar[int] = 95

    req_id: int
    pos: float
    daily_pnl: float
    unrealized_pnl: float
    realized_pnl: float
    value: float

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'PnlSingleMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        return cls(
            req_id=it.next_int(),
            pos=it.next_float(),
            daily_pnl=it.next_float(),
            unrealized_pnl=it.next_float(),
            realized_pnl=it.next_float(),
            value=it.next_float()
        )
