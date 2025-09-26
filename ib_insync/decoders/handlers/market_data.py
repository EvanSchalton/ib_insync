"""Handler functions for market data messages."""

import logging
from typing import Any

from ib_insync.decoders.base import registry
from ib_insync.decoders.models.market_data import (
    HistogramDataMessage,
    PriceSizeTickMessage,
    RealTimeBarMessage,
    TickByTickMessage,
    TickGenericMessage,
    TickOptionComputationMessage,
    TickSizeMessage,
    TickStringMessage,
    UpdateMktDepthL2Message,
    UpdateMktDepthMessage,
)
from ib_insync.objects import HistogramData, OptionComputation, TickAttribBidAsk, TickAttribLast

logger = logging.getLogger(__name__)


@registry.register_handler(PriceSizeTickMessage)
def handle_price_size_tick(wrapper: Any, msg: PriceSizeTickMessage) -> None:
    """
    Handle price/size tick message.

    This combines handling of price and size information.
    """
    if msg.price is not None:
        # Use custom wrapper method if available
        if hasattr(wrapper, 'priceSizeTick'):
            wrapper.priceSizeTick(msg.req_id, msg.tick_type, msg.price, msg.size)
        else:
            # Fall back to standard tickPrice
            wrapper.tickPrice(msg.req_id, msg.tick_type, msg.price, {'size': msg.size})


@registry.register_handler(TickSizeMessage)
def handle_tick_size(wrapper: Any, msg: TickSizeMessage) -> None:
    """Handle tick size message."""
    wrapper.tickSize(msg.req_id, msg.tick_type, msg.size)


@registry.register_handler(TickGenericMessage)
def handle_tick_generic(wrapper: Any, msg: TickGenericMessage) -> None:
    """Handle generic tick message."""
    wrapper.tickGeneric(msg.req_id, msg.tick_type, msg.value)


@registry.register_handler(TickStringMessage)
def handle_tick_string(wrapper: Any, msg: TickStringMessage) -> None:
    """Handle string tick message."""
    wrapper.tickString(msg.req_id, msg.tick_type, msg.value)


@registry.register_handler(TickOptionComputationMessage)
def handle_tick_option_computation(wrapper: Any, msg: TickOptionComputationMessage) -> None:
    """Handle option computation tick message."""
    # Create OptionComputation object
    computation = OptionComputation(
        tickAttrib=msg.tick_attrib,
        impliedVol=msg.implied_vol,
        delta=msg.delta,
        optPrice=msg.opt_price,
        pvDividend=msg.pv_dividend,
        gamma=msg.gamma,
        vega=msg.vega,
        theta=msg.theta,
        undPrice=msg.und_price
    )

    wrapper.tickOptionComputation(
        msg.req_id,
        msg.tick_type,
        msg.tick_attrib,
        msg.implied_vol,
        msg.delta,
        msg.opt_price,
        msg.pv_dividend,
        msg.gamma,
        msg.vega,
        msg.theta,
        msg.und_price
    )


@registry.register_handler(RealTimeBarMessage)
def handle_real_time_bar(wrapper: Any, msg: RealTimeBarMessage) -> None:
    """Handle real-time bar message."""
    wrapper.realtimeBar(
        msg.req_id,
        msg.time,
        msg.open,
        msg.high,
        msg.low,
        msg.close,
        msg.volume,
        msg.wap,
        msg.count
    )


@registry.register_handler(HistogramDataMessage)
def handle_histogram_data(wrapper: Any, msg: HistogramDataMessage) -> None:
    """Handle histogram data message."""
    # Convert data points to HistogramData objects
    items = [
        HistogramData(price=price, count=count)
        for price, count in msg.data_points
    ]

    wrapper.histogramData(msg.req_id, items)


@registry.register_handler(UpdateMktDepthMessage)
def handle_update_mkt_depth(wrapper: Any, msg: UpdateMktDepthMessage) -> None:
    """Handle market depth update message."""
    wrapper.updateMktDepth(
        msg.req_id,
        msg.position,
        msg.operation,
        msg.side,
        msg.price,
        msg.size
    )


@registry.register_handler(UpdateMktDepthL2Message)
def handle_update_mkt_depth_l2(wrapper: Any, msg: UpdateMktDepthL2Message) -> None:
    """Handle level 2 market depth update message."""
    wrapper.updateMktDepthL2(
        msg.req_id,
        msg.position,
        msg.market_maker,
        msg.operation,
        msg.side,
        msg.price,
        msg.size,
        msg.is_smart_depth
    )


@registry.register_handler(TickByTickMessage)
def handle_tick_by_tick(wrapper: Any, msg: TickByTickMessage) -> None:
    """Handle tick-by-tick data message."""
    if msg.tick_type in (1, 2):  # Last or AllLast
        attrib = TickAttribLast(
            pastLimit=msg.past_limit or False,
            unreported=msg.unreported or False
        )
        wrapper.tickByTickAllLast(
            msg.req_id,
            msg.tick_type,
            msg.time,
            msg.price,
            msg.size,
            attrib,
            msg.exchange or '',
            msg.special_conditions or ''
        )

    elif msg.tick_type == 3:  # BidAsk
        attrib = TickAttribBidAsk(
            bidPastLow=msg.bid_past_low or False,
            askPastHigh=msg.ask_past_high or False
        )
        wrapper.tickByTickBidAsk(
            msg.req_id,
            msg.time,
            msg.bid_price,
            msg.ask_price,
            msg.bid_size,
            msg.ask_size,
            attrib
        )

    elif msg.tick_type == 4:  # MidPoint
        wrapper.tickByTickMidPoint(
            msg.req_id,
            msg.time,
            msg.mid_point
        )
