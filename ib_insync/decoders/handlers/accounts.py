"""Handler functions for account-related messages."""

import logging
from typing import Any

from ib_insync.decoders.base import registry
from ib_insync.decoders.models.accounts import (
    AccountDownloadEndMessage,
    AccountSummaryEndMessage,
    AccountSummaryMessage,
    AccountUpdateMultiEndMessage,
    AccountUpdateMultiMessage,
    PnlMessage,
    PnlSingleMessage,
    PositionEndMessage,
    PositionMessage,
    PositionMultiEndMessage,
    PositionMultiMessage,
    UpdateAccountTimeMessage,
    UpdateAccountValueMessage,
    UpdatePortfolioMessage,
)

logger = logging.getLogger(__name__)


@registry.register_handler(UpdateAccountValueMessage)
def handle_update_account_value(wrapper: Any, msg: UpdateAccountValueMessage) -> None:
    """Handle update account value message."""
    wrapper.updateAccountValue(
        msg.key,
        msg.value,
        msg.currency,
        msg.account_name
    )


@registry.register_handler(UpdatePortfolioMessage)
def handle_update_portfolio(wrapper: Any, msg: UpdatePortfolioMessage) -> None:
    """Handle update portfolio message."""
    wrapper.updatePortfolio(
        msg.contract,
        msg.position,
        msg.market_price,
        msg.market_value,
        msg.average_cost,
        msg.unrealized_pnl,
        msg.realized_pnl,
        msg.account_name
    )


@registry.register_handler(UpdateAccountTimeMessage)
def handle_update_account_time(wrapper: Any, msg: UpdateAccountTimeMessage) -> None:
    """Handle update account time message."""
    wrapper.updateAccountTime(msg.time_stamp)


@registry.register_handler(AccountDownloadEndMessage)
def handle_account_download_end(wrapper: Any, msg: AccountDownloadEndMessage) -> None:
    """Handle account download end message."""
    wrapper.accountDownloadEnd(msg.account_name)


@registry.register_handler(PositionMessage)
def handle_position(wrapper: Any, msg: PositionMessage) -> None:
    """Handle position message."""
    wrapper.position(
        msg.account,
        msg.contract,
        msg.position,
        msg.avg_cost
    )


@registry.register_handler(PositionEndMessage)
def handle_position_end(wrapper: Any, msg: PositionEndMessage) -> None:
    """Handle position end message."""
    wrapper.positionEnd()


@registry.register_handler(AccountSummaryMessage)
def handle_account_summary(wrapper: Any, msg: AccountSummaryMessage) -> None:
    """Handle account summary message."""
    wrapper.accountSummary(
        msg.req_id,
        msg.account,
        msg.tag,
        msg.value,
        msg.currency
    )


@registry.register_handler(AccountSummaryEndMessage)
def handle_account_summary_end(wrapper: Any, msg: AccountSummaryEndMessage) -> None:
    """Handle account summary end message."""
    wrapper.accountSummaryEnd(msg.req_id)


@registry.register_handler(PositionMultiMessage)
def handle_position_multi(wrapper: Any, msg: PositionMultiMessage) -> None:
    """Handle position multi message."""
    wrapper.positionMulti(
        msg.req_id,
        msg.account,
        msg.model_code,
        msg.contract,
        msg.position,
        msg.avg_cost
    )


@registry.register_handler(PositionMultiEndMessage)
def handle_position_multi_end(wrapper: Any, msg: PositionMultiEndMessage) -> None:
    """Handle position multi end message."""
    wrapper.positionMultiEnd(msg.req_id)


@registry.register_handler(AccountUpdateMultiMessage)
def handle_account_update_multi(wrapper: Any, msg: AccountUpdateMultiMessage) -> None:
    """Handle account update multi message."""
    wrapper.accountUpdateMulti(
        msg.req_id,
        msg.account,
        msg.model_code,
        msg.key,
        msg.value,
        msg.currency
    )


@registry.register_handler(AccountUpdateMultiEndMessage)
def handle_account_update_multi_end(wrapper: Any, msg: AccountUpdateMultiEndMessage) -> None:
    """Handle account update multi end message."""
    wrapper.accountUpdateMultiEnd(msg.req_id)


@registry.register_handler(PnlMessage)
def handle_pnl(wrapper: Any, msg: PnlMessage) -> None:
    """Handle PnL message."""
    wrapper.pnl(
        msg.req_id,
        msg.daily_pnl,
        msg.unrealized_pnl,
        msg.realized_pnl
    )


@registry.register_handler(PnlSingleMessage)
def handle_pnl_single(wrapper: Any, msg: PnlSingleMessage) -> None:
    """Handle PnL single message."""
    wrapper.pnlSingle(
        msg.req_id,
        msg.pos,
        msg.daily_pnl,
        msg.unrealized_pnl,
        msg.realized_pnl,
        msg.value
    )
