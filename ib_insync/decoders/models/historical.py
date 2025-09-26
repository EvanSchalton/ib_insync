"""Pydantic models for historical data messages."""

from datetime import UTC, datetime
from typing import ClassVar

from pydantic import Field

from ib_insync.decoders.base import IBMessage, registry
from ib_insync.decoders.parsers.field_parser import FieldIterator
from ib_insync.objects import (
    BarData,
    HistoricalSession,
    HistoricalTick,
    HistoricalTickBidAsk,
    HistoricalTickLast,
    TickAttribBidAsk,
    TickAttribLast,
)


@registry.register_message(msg_id=17)
class HistoricalDataMessage(IBMessage):
    """Historical data message (msg_id=17)."""

    MESSAGE_ID: ClassVar[int] = 17

    req_id: int
    start_date_str: str
    end_date_str: str
    bars: list[BarData] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'HistoricalDataMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        req_id = it.next_int()
        start_date_str = it.next()
        end_date_str = it.next()
        num_bars = it.next_int()

        bars = []
        for _ in range(num_bars):
            bar = BarData()
            bar.date = it.next()
            bar.open = it.next_float()
            bar.high = it.next_float()
            bar.low = it.next_float()
            bar.close = it.next_float()
            bar.volume = it.next_float()
            bar.average = it.next_float()
            bar.barCount = it.next_int()
            bars.append(bar)

        return cls(
            req_id=req_id,
            start_date_str=start_date_str,
            end_date_str=end_date_str,
            bars=bars
        )


@registry.register_message(msg_id=88)
class HeadTimestampMessage(IBMessage):
    """Head timestamp message (msg_id=88)."""

    MESSAGE_ID: ClassVar[int] = 88

    req_id: int
    head_timestamp: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'HeadTimestampMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        return cls(
            req_id=it.next_int(),
            head_timestamp=it.next()
        )


@registry.register_message(msg_id=90)
class HistoricalDataUpdateMessage(IBMessage):
    """Historical data update message (msg_id=90)."""

    MESSAGE_ID: ClassVar[int] = 90

    req_id: int
    bar: BarData = Field(default_factory=BarData)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'HistoricalDataUpdateMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        req_id = it.next_int()

        bar = BarData()
        bar.barCount = it.next_int()
        bar.date = it.next()
        bar.open = it.next_float()
        bar.close = it.next_float()
        bar.high = it.next_float()
        bar.low = it.next_float()
        bar.average = it.next_float()
        bar.volume = it.next_float()

        return cls(req_id=req_id, bar=bar)


@registry.register_message(msg_id=96)
class HistoricalTicksMessage(IBMessage):
    """Historical ticks message (msg_id=96)."""

    MESSAGE_ID: ClassVar[int] = 96

    req_id: int
    ticks: list[HistoricalTick] = Field(default_factory=list)
    done: bool

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'HistoricalTicksMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        req_id = it.next_int()
        num_ticks = it.next_int()

        ticks = []
        for _ in range(num_ticks):
            time = it.next_int()
            it.skip(1)  # Skip mask
            price = it.next_float()
            size = it.next_float()

            dt = datetime.fromtimestamp(time, UTC)
            tick = HistoricalTick(dt, price, size)
            ticks.append(tick)

        done = it.next_bool()

        return cls(req_id=req_id, ticks=ticks, done=done)


@registry.register_message(msg_id=97)
class HistoricalTicksBidAskMessage(IBMessage):
    """Historical ticks bid/ask message (msg_id=97)."""

    MESSAGE_ID: ClassVar[int] = 97

    req_id: int
    ticks: list[HistoricalTickBidAsk] = Field(default_factory=list)
    done: bool

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'HistoricalTicksBidAskMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        req_id = it.next_int()
        num_ticks = it.next_int()

        ticks = []
        for _ in range(num_ticks):
            time = it.next_int()
            mask = it.next_int()

            attrib = TickAttribBidAsk(
                askPastHigh=bool(mask & 1),
                bidPastLow=bool(mask & 2)
            )

            price_bid = it.next_float()
            price_ask = it.next_float()
            size_bid = it.next_float()
            size_ask = it.next_float()

            dt = datetime.fromtimestamp(time, UTC)
            tick = HistoricalTickBidAsk(
                dt, attrib, price_bid, price_ask, size_bid, size_ask
            )
            ticks.append(tick)

        done = it.next_bool()

        return cls(req_id=req_id, ticks=ticks, done=done)


@registry.register_message(msg_id=98)
class HistoricalTicksLastMessage(IBMessage):
    """Historical ticks last message (msg_id=98)."""

    MESSAGE_ID: ClassVar[int] = 98

    req_id: int
    ticks: list[HistoricalTickLast] = Field(default_factory=list)
    done: bool

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'HistoricalTicksLastMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        req_id = it.next_int()
        num_ticks = it.next_int()

        ticks = []
        for _ in range(num_ticks):
            time = it.next_int()
            mask = it.next_int()

            attrib = TickAttribLast(
                pastLimit=bool(mask & 1),
                unreported=bool(mask & 2)
            )

            price = it.next_float()
            size = it.next_float()
            exchange = it.next()
            special_conditions = it.next()

            dt = datetime.fromtimestamp(time, UTC)
            tick = HistoricalTickLast(
                dt, attrib, price, size, exchange, special_conditions
            )
            ticks.append(tick)

        done = it.next_bool()

        return cls(req_id=req_id, ticks=ticks, done=done)


@registry.register_message(msg_id=106)
class HistoricalScheduleMessage(IBMessage):
    """Historical schedule message (msg_id=106)."""

    MESSAGE_ID: ClassVar[int] = 106

    req_id: int
    start_date_time: str
    end_date_time: str
    time_zone: str
    sessions: list[HistoricalSession] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'HistoricalScheduleMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        req_id = it.next_int()
        start_date_time = it.next()
        end_date_time = it.next()
        time_zone = it.next()
        count = it.next_int()

        sessions = []
        for _ in range(count):
            session = HistoricalSession(
                startDateTime=it.next(),
                endDateTime=it.next(),
                refDate=it.next()
            )
            sessions.append(session)

        return cls(
            req_id=req_id,
            start_date_time=start_date_time,
            end_date_time=end_date_time,
            time_zone=time_zone,
            sessions=sessions
        )
