"""Handler functions for historical data messages."""

import logging
from typing import Any

from ib_insync.decoders.base import registry
from ib_insync.decoders.models.historical import (
    HeadTimestampMessage,
    HistoricalDataMessage,
    HistoricalDataUpdateMessage,
    HistoricalScheduleMessage,
    HistoricalTicksBidAskMessage,
    HistoricalTicksLastMessage,
    HistoricalTicksMessage,
)

logger = logging.getLogger(__name__)


@registry.register_handler(HistoricalDataMessage)
def handle_historical_data(wrapper: Any, msg: HistoricalDataMessage) -> None:
    """Handle historical data message."""
    # Call historicalData for each bar
    for bar in msg.bars:
        wrapper.historicalData(msg.req_id, bar)

    # Call historicalDataEnd
    wrapper.historicalDataEnd(msg.req_id, msg.start_date_str, msg.end_date_str)


@registry.register_handler(HeadTimestampMessage)
def handle_head_timestamp(wrapper: Any, msg: HeadTimestampMessage) -> None:
    """Handle head timestamp message."""
    wrapper.headTimestamp(msg.req_id, msg.head_timestamp)


@registry.register_handler(HistoricalDataUpdateMessage)
def handle_historical_data_update(wrapper: Any, msg: HistoricalDataUpdateMessage) -> None:
    """Handle historical data update message."""
    wrapper.historicalDataUpdate(msg.req_id, msg.bar)


@registry.register_handler(HistoricalTicksMessage)
def handle_historical_ticks(wrapper: Any, msg: HistoricalTicksMessage) -> None:
    """Handle historical ticks message."""
    wrapper.historicalTicks(msg.req_id, msg.ticks, msg.done)


@registry.register_handler(HistoricalTicksBidAskMessage)
def handle_historical_ticks_bid_ask(wrapper: Any, msg: HistoricalTicksBidAskMessage) -> None:
    """Handle historical ticks bid/ask message."""
    wrapper.historicalTicksBidAsk(msg.req_id, msg.ticks, msg.done)


@registry.register_handler(HistoricalTicksLastMessage)
def handle_historical_ticks_last(wrapper: Any, msg: HistoricalTicksLastMessage) -> None:
    """Handle historical ticks last message."""
    wrapper.historicalTicksLast(msg.req_id, msg.ticks, msg.done)


@registry.register_handler(HistoricalScheduleMessage)
def handle_historical_schedule(wrapper: Any, msg: HistoricalScheduleMessage) -> None:
    """Handle historical schedule message."""
    wrapper.historicalSchedule(
        msg.req_id,
        msg.start_date_time,
        msg.end_date_time,
        msg.time_zone,
        msg.sessions
    )
