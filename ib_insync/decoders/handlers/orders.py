"""Handler functions for order-related messages."""

import logging
from typing import Any

from ib_insync.decoders.base import registry
from ib_insync.decoders.models.orders import (
    CompletedOrderMessage,
    CompletedOrdersEndMessage,
    ExecDetailsEndMessage,
    ExecDetailsMessage,
    OpenOrderEndMessage,
    OpenOrderMessage,
    OrderBoundMessage,
    OrderStatusMessage,
)

logger = logging.getLogger(__name__)


@registry.register_handler(OrderStatusMessage)
def handle_order_status(wrapper: Any, msg: OrderStatusMessage) -> None:
    """Handle order status message."""
    wrapper.orderStatus(
        msg.order_id,
        msg.status,
        msg.filled,
        msg.remaining,
        msg.avg_fill_price,
        msg.perm_id,
        msg.parent_id,
        msg.last_fill_price,
        msg.client_id,
        msg.why_held,
        msg.mkt_cap_price
    )


@registry.register_handler(OpenOrderMessage)
def handle_open_order(wrapper: Any, msg: OpenOrderMessage) -> None:
    """Handle open order message."""
    wrapper.openOrder(
        msg.order.orderId,
        msg.contract,
        msg.order,
        msg.order_state
    )


@registry.register_handler(ExecDetailsMessage)
def handle_exec_details(wrapper: Any, msg: ExecDetailsMessage) -> None:
    """Handle execution details message."""
    wrapper.execDetails(
        msg.req_id,
        msg.contract,
        msg.execution
    )


@registry.register_handler(OpenOrderEndMessage)
def handle_open_order_end(wrapper: Any, msg: OpenOrderEndMessage) -> None:
    """Handle open order end message."""
    wrapper.openOrderEnd()


@registry.register_handler(ExecDetailsEndMessage)
def handle_exec_details_end(wrapper: Any, msg: ExecDetailsEndMessage) -> None:
    """Handle execution details end message."""
    wrapper.execDetailsEnd(msg.req_id)


@registry.register_handler(OrderBoundMessage)
def handle_order_bound(wrapper: Any, msg: OrderBoundMessage) -> None:
    """Handle order bound message."""
    wrapper.orderBound(
        msg.order_id,
        msg.api_client_id,
        msg.api_order_id
    )


@registry.register_handler(CompletedOrderMessage)
def handle_completed_order(wrapper: Any, msg: CompletedOrderMessage) -> None:
    """Handle completed order message."""
    wrapper.completedOrder(
        msg.contract,
        msg.order,
        msg.order_state
    )


@registry.register_handler(CompletedOrdersEndMessage)
def handle_completed_orders_end(wrapper: Any, msg: CompletedOrdersEndMessage) -> None:
    """Handle completed orders end message."""
    wrapper.completedOrdersEnd()
