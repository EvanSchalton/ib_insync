"""Pydantic models for miscellaneous messages."""

from typing import ClassVar

from pydantic import Field

from ib_insync.contract import Contract, ContractDescription
from ib_insync.decoders.base import IBMessage, registry
from ib_insync.decoders.parsers.field_parser import FieldIterator
from ib_insync.objects import (
    DepthMktDataDescription,
    FamilyCode,
    NewsProvider,
    PriceIncrement,
    SmartComponent,
    SoftDollarTier,
)


@registry.register_message(msg_id=4)
class ErrorMessage(IBMessage):
    """Error message (msg_id=4)."""

    MESSAGE_ID: ClassVar[int] = 4

    req_id: int
    error_code: int
    error_string: str
    advanced_order_reject_json: str | None = None

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'ErrorMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        req_id = it.next_int()
        error_code = it.next_int()
        error_string = it.next()
        advanced_order_reject_json = ""

        if server_version >= 166:
            advanced_order_reject_json = it.next()

        return cls(
            req_id=req_id,
            error_code=error_code,
            error_string=error_string,
            advanced_order_reject_json=advanced_order_reject_json
        )


@registry.register_message(msg_id=9)
class NextValidIdMessage(IBMessage):
    """Next valid ID message (msg_id=9)."""

    MESSAGE_ID: ClassVar[int] = 9

    order_id: int

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'NextValidIdMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(order_id=it.next_int())


@registry.register_message(msg_id=14)
class UpdateNewsBulletinMessage(IBMessage):
    """Update news bulletin message (msg_id=14)."""

    MESSAGE_ID: ClassVar[int] = 14

    msg_id: int
    msg_type: int
    news_message: str
    origin_exch: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'UpdateNewsBulletinMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(
            msg_id=it.next_int(),
            msg_type=it.next_int(),
            news_message=it.next(),
            origin_exch=it.next()
        )


@registry.register_message(msg_id=15)
class ManagedAccountsMessage(IBMessage):
    """Managed accounts message (msg_id=15)."""

    MESSAGE_ID: ClassVar[int] = 15

    accounts_list: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'ManagedAccountsMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(accounts_list=it.next())


@registry.register_message(msg_id=16)
class ReceiveFAMessage(IBMessage):
    """Receive FA message (msg_id=16)."""

    MESSAGE_ID: ClassVar[int] = 16

    fa_data_type: int
    xml: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'ReceiveFAMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(
            fa_data_type=it.next_int(),
            xml=it.next()
        )


@registry.register_message(msg_id=19)
class ScannerParametersMessage(IBMessage):
    """Scanner parameters message (msg_id=19)."""

    MESSAGE_ID: ClassVar[int] = 19

    xml: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'ScannerParametersMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(xml=it.next())


@registry.register_message(msg_id=47)
class TickEFPMessage(IBMessage):
    """Tick EFP message (msg_id=47)."""

    MESSAGE_ID: ClassVar[int] = 47

    req_id: int
    tick_type: int
    basis_points: float
    formatted_basis_points: str
    total_dividends: float
    hold_days: int
    future_last_trade_date: str
    dividend_impact: float
    dividends_to_last_trade_date: float

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'TickEFPMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(
            req_id=it.next_int(),
            tick_type=it.next_int(),
            basis_points=it.next_float(),
            formatted_basis_points=it.next(),
            total_dividends=it.next_float(),
            hold_days=it.next_int(),
            future_last_trade_date=it.next(),
            dividend_impact=it.next_float(),
            dividends_to_last_trade_date=it.next_float()
        )


@registry.register_message(msg_id=49)
class CurrentTimeMessage(IBMessage):
    """Current time message (msg_id=49)."""

    MESSAGE_ID: ClassVar[int] = 49

    time: int

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'CurrentTimeMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(time=it.next_int())


@registry.register_message(msg_id=51)
class FundamentalDataMessage(IBMessage):
    """Fundamental data message (msg_id=51)."""

    MESSAGE_ID: ClassVar[int] = 51

    req_id: int
    data: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'FundamentalDataMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(
            req_id=it.next_int(),
            data=it.next()
        )


@registry.register_message(msg_id=57)
class TickSnapshotEndMessage(IBMessage):
    """Tick snapshot end message (msg_id=57)."""

    MESSAGE_ID: ClassVar[int] = 57

    req_id: int

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'TickSnapshotEndMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(req_id=it.next_int())


@registry.register_message(msg_id=58)
class MarketDataTypeMessage(IBMessage):
    """Market data type message (msg_id=58)."""

    MESSAGE_ID: ClassVar[int] = 58

    req_id: int
    market_data_type: int

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'MarketDataTypeMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(
            req_id=it.next_int(),
            market_data_type=it.next_int()
        )


@registry.register_message(msg_id=65)
class VerifyMessageAPIMessage(IBMessage):
    """Verify message API message (msg_id=65)."""

    MESSAGE_ID: ClassVar[int] = 65

    api_data: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'VerifyMessageAPIMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(api_data=it.next())


@registry.register_message(msg_id=66)
class VerifyCompletedMessage(IBMessage):
    """Verify completed message (msg_id=66)."""

    MESSAGE_ID: ClassVar[int] = 66

    is_successful: bool
    error_text: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'VerifyCompletedMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(
            is_successful=it.next_bool(),
            error_text=it.next()
        )


@registry.register_message(msg_id=67)
class DisplayGroupListMessage(IBMessage):
    """Display group list message (msg_id=67)."""

    MESSAGE_ID: ClassVar[int] = 67

    req_id: int
    groups: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'DisplayGroupListMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(
            req_id=it.next_int(),
            groups=it.next()
        )


@registry.register_message(msg_id=68)
class DisplayGroupUpdatedMessage(IBMessage):
    """Display group updated message (msg_id=68)."""

    MESSAGE_ID: ClassVar[int] = 68

    req_id: int
    contract_info: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'DisplayGroupUpdatedMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(
            req_id=it.next_int(),
            contract_info=it.next()
        )


@registry.register_message(msg_id=69)
class VerifyAndAuthMessageAPIMessage(IBMessage):
    """Verify and auth message API message (msg_id=69)."""

    MESSAGE_ID: ClassVar[int] = 69

    api_data: str
    xyz_challenge: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'VerifyAndAuthMessageAPIMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(
            api_data=it.next(),
            xyz_challenge=it.next()
        )


@registry.register_message(msg_id=70)
class VerifyAndAuthCompletedMessage(IBMessage):
    """Verify and auth completed message (msg_id=70)."""

    MESSAGE_ID: ClassVar[int] = 70

    is_successful: bool
    error_text: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'VerifyAndAuthCompletedMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(
            is_successful=it.next_bool(),
            error_text=it.next()
        )


@registry.register_message(msg_id=77)
class SoftDollarTiersMessage(IBMessage):
    """Soft dollar tiers message (msg_id=77)."""

    MESSAGE_ID: ClassVar[int] = 77

    req_id: int
    tiers: list[SoftDollarTier] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'SoftDollarTiersMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        req_id = it.next_int()
        num_tiers = it.next_int()

        tiers = []
        for _ in range(num_tiers):
            tier = SoftDollarTier(
                name=it.next(),
                val=it.next(),
                displayName=it.next()
            )
            tiers.append(tier)

        return cls(req_id=req_id, tiers=tiers)


@registry.register_message(msg_id=78)
class FamilyCodesMessage(IBMessage):
    """Family codes message (msg_id=78)."""

    MESSAGE_ID: ClassVar[int] = 78

    family_codes: list[FamilyCode] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'FamilyCodesMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        num_codes = it.next_int()

        family_codes = []
        for _ in range(num_codes):
            code = FamilyCode(
                accountID=it.next(),
                familyCodeStr=it.next()
            )
            family_codes.append(code)

        return cls(family_codes=family_codes)


@registry.register_message(msg_id=79)
class SymbolSamplesMessage(IBMessage):
    """Symbol samples message (msg_id=79)."""

    MESSAGE_ID: ClassVar[int] = 79

    req_id: int
    contract_descriptions: list[ContractDescription] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'SymbolSamplesMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        req_id = it.next_int()
        num_contracts = it.next_int()

        contract_descriptions = []
        for _ in range(num_contracts):
            cd = ContractDescription()
            cd.contract = Contract()
            cd.contract.conId = it.next_int()
            cd.contract.symbol = it.next()
            cd.contract.secType = it.next()
            cd.contract.primaryExchange = it.next()
            cd.contract.currency = it.next()

            num_derivative_sec_types = it.next_int()
            cd.derivativeSecTypes = []
            for _ in range(num_derivative_sec_types):
                cd.derivativeSecTypes.append(it.next())

            if server_version >= 176:
                cd.contract.description = it.next()
                cd.contract.issuerId = it.next()

            contract_descriptions.append(cd)

        return cls(req_id=req_id, contract_descriptions=contract_descriptions)


@registry.register_message(msg_id=80)
class MktDepthExchangesMessage(IBMessage):
    """Market depth exchanges message (msg_id=80)."""

    MESSAGE_ID: ClassVar[int] = 80

    descriptions: list[DepthMktDataDescription] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'MktDepthExchangesMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        num_descriptions = it.next_int()

        descriptions = []
        for _ in range(num_descriptions):
            desc = DepthMktDataDescription(
                exchange=it.next(),
                secType=it.next(),
                listingExch=it.next(),
                serviceDataType=it.next(),
                aggGroup=it.next_int()
            )
            descriptions.append(desc)

        return cls(descriptions=descriptions)


@registry.register_message(msg_id=81)
class TickReqParamsMessage(IBMessage):
    """Tick req params message (msg_id=81)."""

    MESSAGE_ID: ClassVar[int] = 81

    req_id: int
    min_tick: float
    bbo_exchange: str
    snapshot_permissions: int

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'TickReqParamsMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        return cls(
            req_id=it.next_int(),
            min_tick=it.next_float(),
            bbo_exchange=it.next(),
            snapshot_permissions=it.next_int()
        )


@registry.register_message(msg_id=82)
class SmartComponentsMessage(IBMessage):
    """Smart components message (msg_id=82)."""

    MESSAGE_ID: ClassVar[int] = 82

    req_id: int
    components: list[SmartComponent] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'SmartComponentsMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        req_id = it.next_int()
        num_components = it.next_int()

        components = []
        for _ in range(num_components):
            component = SmartComponent(
                bitNumber=it.next_int(),
                exchange=it.next(),
                exchangeLetter=it.next()
            )
            components.append(component)

        return cls(req_id=req_id, components=components)


@registry.register_message(msg_id=83)
class NewsArticleMessage(IBMessage):
    """News article message (msg_id=83)."""

    MESSAGE_ID: ClassVar[int] = 83

    req_id: int
    article_type: int
    article_text: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'NewsArticleMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        return cls(
            req_id=it.next_int(),
            article_type=it.next_int(),
            article_text=it.next()
        )


@registry.register_message(msg_id=84)
class TickNewsMessage(IBMessage):
    """Tick news message (msg_id=84)."""

    MESSAGE_ID: ClassVar[int] = 84

    req_id: int
    time_stamp: int
    provider_code: str
    article_id: str
    headline: str
    extra_data: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'TickNewsMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        return cls(
            req_id=it.next_int(),
            time_stamp=it.next_int(),
            provider_code=it.next(),
            article_id=it.next(),
            headline=it.next(),
            extra_data=it.next()
        )


@registry.register_message(msg_id=85)
class NewsProvidersMessage(IBMessage):
    """News providers message (msg_id=85)."""

    MESSAGE_ID: ClassVar[int] = 85

    providers: list[NewsProvider] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'NewsProvidersMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        num_providers = it.next_int()

        providers = []
        for _ in range(num_providers):
            provider = NewsProvider(
                code=it.next(),
                name=it.next()
            )
            providers.append(provider)

        return cls(providers=providers)


@registry.register_message(msg_id=86)
class HistoricalNewsMessage(IBMessage):
    """Historical news message (msg_id=86)."""

    MESSAGE_ID: ClassVar[int] = 86

    req_id: int
    time: str
    provider_code: str
    article_id: str
    headline: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'HistoricalNewsMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        return cls(
            req_id=it.next_int(),
            time=it.next(),
            provider_code=it.next(),
            article_id=it.next(),
            headline=it.next()
        )


@registry.register_message(msg_id=87)
class HistoricalNewsEndMessage(IBMessage):
    """Historical news end message (msg_id=87)."""

    MESSAGE_ID: ClassVar[int] = 87

    req_id: int
    has_more: bool

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'HistoricalNewsEndMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        return cls(
            req_id=it.next_int(),
            has_more=it.next_bool()
        )


@registry.register_message(msg_id=91)
class RerouteMktDataReqMessage(IBMessage):
    """Reroute market data req message (msg_id=91)."""

    MESSAGE_ID: ClassVar[int] = 91

    req_id: int
    con_id: int
    exchange: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'RerouteMktDataReqMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        return cls(
            req_id=it.next_int(),
            con_id=it.next_int(),
            exchange=it.next()
        )


@registry.register_message(msg_id=92)
class RerouteMktDepthReqMessage(IBMessage):
    """Reroute market depth req message (msg_id=92)."""

    MESSAGE_ID: ClassVar[int] = 92

    req_id: int
    con_id: int
    exchange: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'RerouteMktDepthReqMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        return cls(
            req_id=it.next_int(),
            con_id=it.next_int(),
            exchange=it.next()
        )


@registry.register_message(msg_id=93)
class MarketRuleMessage(IBMessage):
    """Market rule message (msg_id=93)."""

    MESSAGE_ID: ClassVar[int] = 93

    market_rule_id: int
    price_increments: list[PriceIncrement] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'MarketRuleMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        market_rule_id = it.next_int()
        num_increments = it.next_int()

        price_increments = []
        for _ in range(num_increments):
            increment = PriceIncrement(
                lowEdge=it.next_float(),
                increment=it.next_float()
            )
            price_increments.append(increment)

        return cls(market_rule_id=market_rule_id, price_increments=price_increments)


@registry.register_message(msg_id=103)
class ReplaceFAEndMessage(IBMessage):
    """Replace FA end message (msg_id=103)."""

    MESSAGE_ID: ClassVar[int] = 103

    req_id: int
    text: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'ReplaceFAEndMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        return cls(
            req_id=it.next_int(),
            text=it.next()
        )


@registry.register_message(msg_id=104)
class WshMetaDataMessage(IBMessage):
    """WSH meta data message (msg_id=104)."""

    MESSAGE_ID: ClassVar[int] = 104

    req_id: int
    data_json: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'WshMetaDataMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        return cls(
            req_id=it.next_int(),
            data_json=it.next()
        )


@registry.register_message(msg_id=105)
class WshEventDataMessage(IBMessage):
    """WSH event data message (msg_id=105)."""

    MESSAGE_ID: ClassVar[int] = 105

    req_id: int
    data_json: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'WshEventDataMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        return cls(
            req_id=it.next_int(),
            data_json=it.next()
        )


@registry.register_message(msg_id=107)
class UserInfoMessage(IBMessage):
    """User info message (msg_id=107)."""

    MESSAGE_ID: ClassVar[int] = 107

    req_id: int
    white_branding_id: str

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'UserInfoMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        return cls(
            req_id=it.next_int(),
            white_branding_id=it.next()
        )
