"""Pydantic models for contract-related messages."""

from typing import ClassVar

from pydantic import Field

from ib_insync.contract import Contract, ContractDetails, DeltaNeutralContract, TagValue
from ib_insync.decoders.base import IBMessage, registry
from ib_insync.decoders.parsers.field_parser import FieldIterator
from ib_insync.objects import CommissionReport


@registry.register_message(msg_id=10)
class ContractDetailsMessage(IBMessage):
    """Contract details message (msg_id=10)."""

    MESSAGE_ID: ClassVar[int] = 10

    req_id: int
    contract_details: ContractDetails = Field(default_factory=ContractDetails)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'ContractDetailsMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        cd = ContractDetails()
        cd.contract = c = Contract()

        if server_version < 164:
            it.skip(1)  # Skip obsolete field

        req_id = it.next_int()
        c.symbol = it.next()
        c.secType = it.next()
        last_times = it.next()
        c.strike = it.next_float()
        c.right = it.next()
        c.exchange = it.next()
        c.currency = it.next()
        c.localSymbol = it.next()
        cd.marketName = it.next()
        c.tradingClass = it.next()
        c.conId = it.next_int()
        cd.minTick = it.next_float()

        if server_version < 164:
            it.skip(1)  # Skip obsolete mdSizeMultiplier

        c.multiplier = it.next()
        cd.orderTypes = it.next()
        cd.validExchanges = it.next()
        cd.priceMagnifier = it.next_int()
        cd.underConId = it.next_int()
        cd.longName = it.next()
        c.primaryExchange = it.next()
        cd.contractMonth = it.next()
        cd.industry = it.next()
        cd.category = it.next()
        cd.subcategory = it.next()
        cd.timeZoneId = it.next()
        cd.tradingHours = it.next()
        cd.liquidHours = it.next()
        cd.evRule = it.next()
        cd.evMultiplier = it.next_int()

        # Parse security IDs
        num_sec_ids = it.next_int()
        if num_sec_ids > 0:
            cd.secIdList = []
            for _ in range(num_sec_ids):
                tag = it.next()
                value = it.next()
                cd.secIdList.append(TagValue(tag, value))

        cd.aggGroup = it.next_int()
        cd.underSymbol = it.next()
        cd.underSecType = it.next()
        cd.marketRuleIds = it.next()
        cd.realExpirationDate = it.next()
        cd.stockType = it.next()

        if server_version == 163:
            cd.suggestedSizeIncrement = it.next_float()

        if server_version >= 164:
            cd.minSize = it.next_float()
            cd.sizeIncrement = it.next_float()
            cd.suggestedSizeIncrement = it.next_float()
            # Skip minCashQtySize

        # Parse last trade date and time
        times = last_times.split('-' if '-' in last_times else None)
        if len(times) > 0:
            c.lastTradeDateOrContractMonth = times[0]
        if len(times) > 1:
            cd.lastTradeTime = times[1]
        if len(times) > 2:
            cd.timeZoneId = times[2]

        # Decode Unicode escape sequences in long name
        cd.longName = cd.longName.encode().decode('unicode-escape')

        return cls(req_id=req_id, contract_details=cd)


@registry.register_message(msg_id=18)
class BondContractDetailsMessage(IBMessage):
    """Bond contract details message (msg_id=18)."""

    MESSAGE_ID: ClassVar[int] = 18

    req_id: int
    contract_details: ContractDetails = Field(default_factory=ContractDetails)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'BondContractDetailsMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        cd = ContractDetails()
        cd.contract = c = Contract()

        if server_version < 164:
            it.skip(1)  # Skip obsolete field

        req_id = it.next_int()
        c.symbol = it.next()
        c.secType = it.next()
        cd.cusip = it.next()
        cd.coupon = it.next_float()
        last_times = it.next()
        cd.issueDate = it.next()
        cd.ratings = it.next()
        cd.bondType = it.next()
        cd.couponType = it.next()
        cd.convertible = it.next_bool()
        cd.callable = it.next_bool()
        cd.putable = it.next_bool()
        cd.descAppend = it.next()
        c.exchange = it.next()
        c.currency = it.next()
        cd.marketName = it.next()
        c.tradingClass = it.next()
        c.conId = it.next_int()
        cd.minTick = it.next_float()

        if server_version < 164:
            it.skip(1)  # Skip obsolete mdSizeMultiplier

        cd.orderTypes = it.next()
        cd.validExchanges = it.next()
        cd.nextOptionDate = it.next()
        cd.nextOptionType = it.next()
        cd.nextOptionPartial = it.next_bool()
        cd.notes = it.next()
        cd.longName = it.next()
        cd.evRule = it.next()
        cd.evMultiplier = it.next_int()

        # Parse security IDs
        num_sec_ids = it.next_int()
        if num_sec_ids > 0:
            cd.secIdList = []
            for _ in range(num_sec_ids):
                tag = it.next()
                value = it.next()
                cd.secIdList.append(TagValue(tag, value))

        cd.aggGroup = it.next_int()
        cd.marketRuleIds = it.next()

        if server_version >= 164:
            cd.minSize = it.next_float()
            cd.sizeIncrement = it.next_float()
            cd.suggestedSizeIncrement = it.next_float()

        # Parse last trade date and time
        times = last_times.split('-' if '-' in last_times else None)
        if len(times) > 0:
            cd.maturity = times[0]
        if len(times) > 1:
            cd.lastTradeTime = times[1]
        if len(times) > 2:
            cd.timeZoneId = times[2]

        return cls(req_id=req_id, contract_details=cd)


@registry.register_message(msg_id=20)
class ScannerDataMessage(IBMessage):
    """Scanner data message (msg_id=20)."""

    MESSAGE_ID: ClassVar[int] = 20

    req_id: int
    contracts: list[ContractDetails] = Field(default_factory=list)
    ranks: list[int] = Field(default_factory=list)
    distances: list[str] = Field(default_factory=list)
    benchmarks: list[str] = Field(default_factory=list)
    projections: list[str] = Field(default_factory=list)
    legs_strs: list[str] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'ScannerDataMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        req_id = it.next_int()
        num_contracts = it.next_int()

        contracts = []
        ranks = []
        distances = []
        benchmarks = []
        projections = []
        legs_strs = []

        for _ in range(num_contracts):
            cd = ContractDetails()
            cd.contract = c = Contract()

            rank = it.next_int()
            c.conId = it.next_int()
            c.symbol = it.next()
            c.secType = it.next()
            c.lastTradeDateOrContractMonth = it.next()
            c.strike = it.next_float()
            c.right = it.next()
            c.exchange = it.next()
            c.currency = it.next()
            c.localSymbol = it.next()
            cd.marketName = it.next()
            c.tradingClass = it.next()
            distance = it.next()
            benchmark = it.next()
            projection = it.next()
            legs_str = it.next()

            contracts.append(cd)
            ranks.append(rank)
            distances.append(distance)
            benchmarks.append(benchmark)
            projections.append(projection)
            legs_strs.append(legs_str)

        return cls(
            req_id=req_id,
            contracts=contracts,
            ranks=ranks,
            distances=distances,
            benchmarks=benchmarks,
            projections=projections,
            legs_strs=legs_strs
        )


@registry.register_message(msg_id=52)
class ContractDetailsEndMessage(IBMessage):
    """Contract details end message (msg_id=52)."""

    MESSAGE_ID: ClassVar[int] = 52

    req_id: int

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'ContractDetailsEndMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(req_id=it.next_int())


@registry.register_message(msg_id=56)
class DeltaNeutralValidationMessage(IBMessage):
    """Delta neutral validation message (msg_id=56)."""

    MESSAGE_ID: ClassVar[int] = 56

    req_id: int
    delta_neutral_contract: DeltaNeutralContract = Field(default_factory=DeltaNeutralContract)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'DeltaNeutralValidationMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        req_id = it.next_int()
        con_id = it.next_int()
        delta = it.next_float()
        price = it.next_float()

        dnc = DeltaNeutralContract()
        dnc.conId = con_id
        dnc.delta = delta
        dnc.price = price

        return cls(req_id=req_id, delta_neutral_contract=dnc)


@registry.register_message(msg_id=59)
class CommissionReportMessage(IBMessage):
    """Commission report message (msg_id=59)."""

    MESSAGE_ID: ClassVar[int] = 59

    commission_report: CommissionReport = Field(default_factory=CommissionReport)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'CommissionReportMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        exec_id = it.next()
        commission = it.next_float()
        currency = it.next()
        realized_pnl = it.next_float()
        yield_ = it.next_float()
        yield_redemption_date = it.next_int()

        commission_report = CommissionReport()
        commission_report.execId = exec_id
        commission_report.commission = commission
        commission_report.currency = currency
        commission_report.realizedPNL = realized_pnl
        commission_report.yield_ = yield_
        commission_report.yieldRedemptionDate = yield_redemption_date

        return cls(commission_report=commission_report)


@registry.register_message(msg_id=75)
class SecurityDefinitionOptionParameterMessage(IBMessage):
    """Security definition option parameter message (msg_id=75)."""

    MESSAGE_ID: ClassVar[int] = 75

    req_id: int
    exchange: str
    underlying_con_id: int
    trading_class: str
    multiplier: str
    expirations: list[str] = Field(default_factory=list)
    strikes: list[float] = Field(default_factory=list)

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'SecurityDefinitionOptionParameterMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        req_id = it.next_int()
        exchange = it.next()
        underlying_con_id = it.next_int()
        trading_class = it.next()
        multiplier = it.next()
        num_expirations = it.next_int()

        expirations = []
        for _ in range(num_expirations):
            expirations.append(it.next())

        num_strikes = it.next_int()
        strikes = []
        for _ in range(num_strikes):
            strikes.append(it.next_float())

        return cls(
            req_id=req_id,
            exchange=exchange,
            underlying_con_id=underlying_con_id,
            trading_class=trading_class,
            multiplier=multiplier,
            expirations=expirations,
            strikes=strikes
        )


@registry.register_message(msg_id=76)
class SecurityDefinitionOptionParameterEndMessage(IBMessage):
    """Security definition option parameter end message (msg_id=76)."""

    MESSAGE_ID: ClassVar[int] = 76

    req_id: int

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'SecurityDefinitionOptionParameterEndMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        return cls(req_id=it.next_int())
