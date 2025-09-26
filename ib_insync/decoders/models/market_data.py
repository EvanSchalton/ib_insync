"""Pydantic models for market data messages."""

from typing import ClassVar

from pydantic import Field

from ib_insync.decoders.base import IBMessage, registry
from ib_insync.decoders.parsers.field_parser import FieldIterator


@registry.register_message(msg_id=1)
class PriceSizeTickMessage(IBMessage):
    """
    Price/Size tick message (msg_id=1).

    This combines price and size information for various tick types.
    """

    MESSAGE_ID: ClassVar[int] = 1

    req_id: int
    tick_type: int
    price: float | None = None
    size: float = 0.0

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'PriceSizeTickMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        req_id = it.next_int()
        tick_type = it.next_int()
        price = it.next()
        size = it.next()

        # Don't create message if price is empty
        if not price:
            return None

        return cls(
            req_id=req_id,
            tick_type=tick_type,
            price=float(price),
            size=float(size) if size else 0.0
        )


@registry.register_message(msg_id=2)
class TickSizeMessage(IBMessage):
    """Tick size message (msg_id=2)."""

    MESSAGE_ID: ClassVar[int] = 2

    req_id: int
    tick_type: int
    size: float

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'TickSizeMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(
            req_id=it.next_int(),
            tick_type=it.next_int(),
            size=it.next_float()
        )


@registry.register_message(msg_id=45)
class TickGenericMessage(IBMessage):
    """Generic tick message (msg_id=45)."""

    MESSAGE_ID: ClassVar[int] = 45

    req_id: int
    tick_type: int
    value: float

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'TickGenericMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(
            req_id=it.next_int(),
            tick_type=it.next_int(),
            value=it.next_float()
        )


@registry.register_message(msg_id=46)
class TickStringMessage(IBMessage):
    """String tick message (msg_id=46)."""

    MESSAGE_ID: ClassVar[int] = 46

    req_id: int
    tick_type: int
    value: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'TickStringMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(
            req_id=it.next_int(),
            tick_type=it.next_int(),
            value=it.next()
        )


@registry.register_message(msg_id=21)
class TickOptionComputationMessage(IBMessage):
    """Option computation tick message (msg_id=21)."""

    MESSAGE_ID: ClassVar[int] = 21

    req_id: int
    tick_type: int
    tick_attrib: int
    implied_vol: float | None = None
    delta: float | None = None
    opt_price: float | None = None
    pv_dividend: float | None = None
    gamma: float | None = None
    vega: float | None = None
    theta: float | None = None
    und_price: float | None = None

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'TickOptionComputationMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        req_id = it.next_int()
        tick_type = it.next_int()
        tick_attrib = it.next_int()

        # Parse optional values (-1 means not computed)
        def parse_opt_float(value: str) -> float | None:
            if not value or float(value) < 0:
                return None
            return float(value)

        return cls(
            req_id=req_id,
            tick_type=tick_type,
            tick_attrib=tick_attrib,
            implied_vol=parse_opt_float(it.next()),
            delta=parse_opt_float(it.next()),
            opt_price=parse_opt_float(it.next()),
            pv_dividend=parse_opt_float(it.next()),
            gamma=parse_opt_float(it.next()),
            vega=parse_opt_float(it.next()),
            theta=parse_opt_float(it.next()),
            und_price=parse_opt_float(it.next())
        )


@registry.register_message(msg_id=50)
class RealTimeBarMessage(IBMessage):
    """Real-time bar message (msg_id=50)."""

    MESSAGE_ID: ClassVar[int] = 50

    req_id: int
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    wap: float
    count: int

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'RealTimeBarMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(
            req_id=it.next_int(),
            time=it.next_int(),
            open=it.next_float(),
            high=it.next_float(),
            low=it.next_float(),
            close=it.next_float(),
            volume=it.next_float(),
            wap=it.next_float(),
            count=it.next_int()
        )


@registry.register_message(msg_id=89)
class HistogramDataMessage(IBMessage):
    """Histogram data message (msg_id=89)."""

    MESSAGE_ID: ClassVar[int] = 89

    req_id: int
    num_points: int
    data_points: list[tuple[float, int]] = Field(default_factory=list)

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'HistogramDataMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        req_id = it.next_int()
        num_points = it.next_int()

        data_points = []
        for _ in range(num_points):
            price = it.next_float()
            count = it.next_int()
            data_points.append((price, count))

        return cls(
            req_id=req_id,
            num_points=num_points,
            data_points=data_points
        )


@registry.register_message(msg_id=12)
class UpdateMktDepthMessage(IBMessage):
    """Market depth update message (msg_id=12)."""

    MESSAGE_ID: ClassVar[int] = 12

    req_id: int
    position: int
    operation: int
    side: int
    price: float
    size: float

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'UpdateMktDepthMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(
            req_id=it.next_int(),
            position=it.next_int(),
            operation=it.next_int(),
            side=it.next_int(),
            price=it.next_float(),
            size=it.next_float()
        )


@registry.register_message(msg_id=13)
class UpdateMktDepthL2Message(IBMessage):
    """Level 2 market depth update message (msg_id=13)."""

    MESSAGE_ID: ClassVar[int] = 13

    req_id: int
    position: int
    market_maker: str
    operation: int
    side: int
    price: float
    size: float
    is_smart_depth: bool

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'UpdateMktDepthL2Message':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(
            req_id=it.next_int(),
            position=it.next_int(),
            market_maker=it.next(),
            operation=it.next_int(),
            side=it.next_int(),
            price=it.next_float(),
            size=it.next_float(),
            is_smart_depth=it.next_bool()
        )


@registry.register_message(msg_id=99)
class TickByTickMessage(IBMessage):
    """Tick-by-tick data message (msg_id=99)."""

    MESSAGE_ID: ClassVar[int] = 99

    req_id: int
    tick_type: int  # 1=Last, 2=AllLast, 3=BidAsk, 4=MidPoint
    time: int

    # Fields for Last/AllLast
    price: float | None = None
    size: float | None = None
    exchange: str | None = None
    special_conditions: str | None = None
    past_limit: bool | None = None
    unreported: bool | None = None

    # Fields for BidAsk
    bid_price: float | None = None
    ask_price: float | None = None
    bid_size: float | None = None
    ask_size: float | None = None
    bid_past_low: bool | None = None
    ask_past_high: bool | None = None

    # Fields for MidPoint
    mid_point: float | None = None

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'TickByTickMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        req_id = it.next_int()
        tick_type = it.next_int()
        time = it.next_int()

        message = cls(req_id=req_id, tick_type=tick_type, time=time)

        if tick_type in (1, 2):  # Last or AllLast
            message.price = it.next_float()
            message.size = it.next_float()
            mask = it.next_int()
            message.past_limit = bool(mask & 1)
            message.unreported = bool(mask & 2)
            message.exchange = it.next()
            message.special_conditions = it.next()

        elif tick_type == 3:  # BidAsk
            message.bid_price = it.next_float()
            message.ask_price = it.next_float()
            message.bid_size = it.next_float()
            message.ask_size = it.next_float()
            mask = it.next_int()
            message.bid_past_low = bool(mask & 1)
            message.ask_past_high = bool(mask & 2)

        elif tick_type == 4:  # MidPoint
            message.mid_point = it.next_float()

        return message
