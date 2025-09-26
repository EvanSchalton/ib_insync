"""Handler functions for miscellaneous messages."""

import logging
from typing import Any

from ib_insync.decoders.base import registry
from ib_insync.decoders.models.misc import (
    CurrentTimeMessage,
    DisplayGroupListMessage,
    DisplayGroupUpdatedMessage,
    ErrorMessage,
    FamilyCodesMessage,
    FundamentalDataMessage,
    HistoricalNewsEndMessage,
    HistoricalNewsMessage,
    ManagedAccountsMessage,
    MarketDataTypeMessage,
    MarketRuleMessage,
    MktDepthExchangesMessage,
    NewsArticleMessage,
    NewsProvidersMessage,
    NextValidIdMessage,
    ReceiveFAMessage,
    ReplaceFAEndMessage,
    RerouteMktDataReqMessage,
    RerouteMktDepthReqMessage,
    ScannerParametersMessage,
    SmartComponentsMessage,
    SoftDollarTiersMessage,
    SymbolSamplesMessage,
    TickEFPMessage,
    TickNewsMessage,
    TickReqParamsMessage,
    TickSnapshotEndMessage,
    UpdateNewsBulletinMessage,
    UserInfoMessage,
    VerifyAndAuthCompletedMessage,
    VerifyAndAuthMessageAPIMessage,
    VerifyCompletedMessage,
    VerifyMessageAPIMessage,
    WshEventDataMessage,
    WshMetaDataMessage,
)

logger = logging.getLogger(__name__)


@registry.register_handler(ErrorMessage)
def handle_error(wrapper: Any, msg: ErrorMessage) -> None:
    """Handle error message."""
    wrapper.error(
        msg.req_id,
        msg.error_code,
        msg.error_string,
        msg.advanced_order_reject_json
    )


@registry.register_handler(NextValidIdMessage)
def handle_next_valid_id(wrapper: Any, msg: NextValidIdMessage) -> None:
    """Handle next valid ID message."""
    wrapper.nextValidId(msg.order_id)


@registry.register_handler(UpdateNewsBulletinMessage)
def handle_update_news_bulletin(wrapper: Any, msg: UpdateNewsBulletinMessage) -> None:
    """Handle update news bulletin message."""
    wrapper.updateNewsBulletin(
        msg.msg_id,
        msg.msg_type,
        msg.news_message,
        msg.origin_exch
    )


@registry.register_handler(ManagedAccountsMessage)
def handle_managed_accounts(wrapper: Any, msg: ManagedAccountsMessage) -> None:
    """Handle managed accounts message."""
    wrapper.managedAccounts(msg.accounts_list)


@registry.register_handler(ReceiveFAMessage)
def handle_receive_fa(wrapper: Any, msg: ReceiveFAMessage) -> None:
    """Handle receive FA message."""
    wrapper.receiveFA(msg.fa_data_type, msg.xml)


@registry.register_handler(ScannerParametersMessage)
def handle_scanner_parameters(wrapper: Any, msg: ScannerParametersMessage) -> None:
    """Handle scanner parameters message."""
    wrapper.scannerParameters(msg.xml)


@registry.register_handler(TickEFPMessage)
def handle_tick_efp(wrapper: Any, msg: TickEFPMessage) -> None:
    """Handle tick EFP message."""
    wrapper.tickEFP(
        msg.req_id,
        msg.tick_type,
        msg.basis_points,
        msg.formatted_basis_points,
        msg.total_dividends,
        msg.hold_days,
        msg.future_last_trade_date,
        msg.dividend_impact,
        msg.dividends_to_last_trade_date
    )


@registry.register_handler(CurrentTimeMessage)
def handle_current_time(wrapper: Any, msg: CurrentTimeMessage) -> None:
    """Handle current time message."""
    wrapper.currentTime(msg.time)


@registry.register_handler(FundamentalDataMessage)
def handle_fundamental_data(wrapper: Any, msg: FundamentalDataMessage) -> None:
    """Handle fundamental data message."""
    wrapper.fundamentalData(msg.req_id, msg.data)


@registry.register_handler(TickSnapshotEndMessage)
def handle_tick_snapshot_end(wrapper: Any, msg: TickSnapshotEndMessage) -> None:
    """Handle tick snapshot end message."""
    wrapper.tickSnapshotEnd(msg.req_id)


@registry.register_handler(MarketDataTypeMessage)
def handle_market_data_type(wrapper: Any, msg: MarketDataTypeMessage) -> None:
    """Handle market data type message."""
    wrapper.marketDataType(msg.req_id, msg.market_data_type)


@registry.register_handler(VerifyMessageAPIMessage)
def handle_verify_message_api(wrapper: Any, msg: VerifyMessageAPIMessage) -> None:
    """Handle verify message API message."""
    wrapper.verifyMessageAPI(msg.api_data)


@registry.register_handler(VerifyCompletedMessage)
def handle_verify_completed(wrapper: Any, msg: VerifyCompletedMessage) -> None:
    """Handle verify completed message."""
    wrapper.verifyCompleted(msg.is_successful, msg.error_text)


@registry.register_handler(DisplayGroupListMessage)
def handle_display_group_list(wrapper: Any, msg: DisplayGroupListMessage) -> None:
    """Handle display group list message."""
    wrapper.displayGroupList(msg.req_id, msg.groups)


@registry.register_handler(DisplayGroupUpdatedMessage)
def handle_display_group_updated(wrapper: Any, msg: DisplayGroupUpdatedMessage) -> None:
    """Handle display group updated message."""
    wrapper.displayGroupUpdated(msg.req_id, msg.contract_info)


@registry.register_handler(VerifyAndAuthMessageAPIMessage)
def handle_verify_and_auth_message_api(wrapper: Any, msg: VerifyAndAuthMessageAPIMessage) -> None:
    """Handle verify and auth message API message."""
    wrapper.verifyAndAuthMessageAPI(msg.api_data, msg.xyz_challenge)


@registry.register_handler(VerifyAndAuthCompletedMessage)
def handle_verify_and_auth_completed(wrapper: Any, msg: VerifyAndAuthCompletedMessage) -> None:
    """Handle verify and auth completed message."""
    wrapper.verifyAndAuthCompleted(msg.is_successful, msg.error_text)


@registry.register_handler(SoftDollarTiersMessage)
def handle_soft_dollar_tiers(wrapper: Any, msg: SoftDollarTiersMessage) -> None:
    """Handle soft dollar tiers message."""
    wrapper.softDollarTiers(msg.req_id, msg.tiers)


@registry.register_handler(FamilyCodesMessage)
def handle_family_codes(wrapper: Any, msg: FamilyCodesMessage) -> None:
    """Handle family codes message."""
    wrapper.familyCodes(msg.family_codes)


@registry.register_handler(SymbolSamplesMessage)
def handle_symbol_samples(wrapper: Any, msg: SymbolSamplesMessage) -> None:
    """Handle symbol samples message."""
    wrapper.symbolSamples(msg.req_id, msg.contract_descriptions)


@registry.register_handler(MktDepthExchangesMessage)
def handle_mkt_depth_exchanges(wrapper: Any, msg: MktDepthExchangesMessage) -> None:
    """Handle market depth exchanges message."""
    wrapper.mktDepthExchanges(msg.descriptions)


@registry.register_handler(TickReqParamsMessage)
def handle_tick_req_params(wrapper: Any, msg: TickReqParamsMessage) -> None:
    """Handle tick req params message."""
    wrapper.tickReqParams(
        msg.req_id,
        msg.min_tick,
        msg.bbo_exchange,
        msg.snapshot_permissions
    )


@registry.register_handler(SmartComponentsMessage)
def handle_smart_components(wrapper: Any, msg: SmartComponentsMessage) -> None:
    """Handle smart components message."""
    wrapper.smartComponents(msg.req_id, msg.components)


@registry.register_handler(NewsArticleMessage)
def handle_news_article(wrapper: Any, msg: NewsArticleMessage) -> None:
    """Handle news article message."""
    wrapper.newsArticle(msg.req_id, msg.article_type, msg.article_text)


@registry.register_handler(TickNewsMessage)
def handle_tick_news(wrapper: Any, msg: TickNewsMessage) -> None:
    """Handle tick news message."""
    wrapper.tickNews(
        msg.req_id,
        msg.time_stamp,
        msg.provider_code,
        msg.article_id,
        msg.headline,
        msg.extra_data
    )


@registry.register_handler(NewsProvidersMessage)
def handle_news_providers(wrapper: Any, msg: NewsProvidersMessage) -> None:
    """Handle news providers message."""
    wrapper.newsProviders(msg.providers)


@registry.register_handler(HistoricalNewsMessage)
def handle_historical_news(wrapper: Any, msg: HistoricalNewsMessage) -> None:
    """Handle historical news message."""
    wrapper.historicalNews(
        msg.req_id,
        msg.time,
        msg.provider_code,
        msg.article_id,
        msg.headline
    )


@registry.register_handler(HistoricalNewsEndMessage)
def handle_historical_news_end(wrapper: Any, msg: HistoricalNewsEndMessage) -> None:
    """Handle historical news end message."""
    wrapper.historicalNewsEnd(msg.req_id, msg.has_more)


@registry.register_handler(RerouteMktDataReqMessage)
def handle_reroute_mkt_data_req(wrapper: Any, msg: RerouteMktDataReqMessage) -> None:
    """Handle reroute market data req message."""
    wrapper.rerouteMktDataReq(msg.req_id, msg.con_id, msg.exchange)


@registry.register_handler(RerouteMktDepthReqMessage)
def handle_reroute_mkt_depth_req(wrapper: Any, msg: RerouteMktDepthReqMessage) -> None:
    """Handle reroute market depth req message."""
    wrapper.rerouteMktDepthReq(msg.req_id, msg.con_id, msg.exchange)


@registry.register_handler(MarketRuleMessage)
def handle_market_rule(wrapper: Any, msg: MarketRuleMessage) -> None:
    """Handle market rule message."""
    wrapper.marketRule(msg.market_rule_id, msg.price_increments)


@registry.register_handler(ReplaceFAEndMessage)
def handle_replace_fa_end(wrapper: Any, msg: ReplaceFAEndMessage) -> None:
    """Handle replace FA end message."""
    wrapper.replaceFAEnd(msg.req_id, msg.text)


@registry.register_handler(WshMetaDataMessage)
def handle_wsh_meta_data(wrapper: Any, msg: WshMetaDataMessage) -> None:
    """Handle WSH meta data message."""
    wrapper.wshMetaData(msg.req_id, msg.data_json)


@registry.register_handler(WshEventDataMessage)
def handle_wsh_event_data(wrapper: Any, msg: WshEventDataMessage) -> None:
    """Handle WSH event data message."""
    wrapper.wshEventData(msg.req_id, msg.data_json)


@registry.register_handler(UserInfoMessage)
def handle_user_info(wrapper: Any, msg: UserInfoMessage) -> None:
    """Handle user info message."""
    wrapper.userInfo(msg.req_id, msg.white_branding_id)
