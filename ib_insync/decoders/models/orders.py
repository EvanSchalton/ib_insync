"""Pydantic models for order-related messages."""

from typing import ClassVar

from pydantic import Field

from ib_insync.contract import ComboLeg, Contract, DeltaNeutralContract, TagValue
from ib_insync.decoders.base import IBMessage, registry
from ib_insync.decoders.parsers.field_parser import FieldIterator
from ib_insync.objects import Execution
from ib_insync.order import Order, OrderComboLeg, OrderCondition, OrderState
from ib_insync.util import UNSET_DOUBLE, parseIBDatetime


@registry.register_message(msg_id=3)
class OrderStatusMessage(IBMessage):
    """Order status message (msg_id=3)."""

    MESSAGE_ID: ClassVar[int] = 3

    order_id: int
    status: str
    filled: float
    remaining: float
    avg_fill_price: float
    perm_id: int
    parent_id: int
    last_fill_price: float
    client_id: int
    why_held: str
    mkt_cap_price: float

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'OrderStatusMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        return cls(
            order_id=it.next_int(),
            status=it.next(),
            filled=it.next_float(),
            remaining=it.next_float(),
            avg_fill_price=it.next_float(),
            perm_id=it.next_int(),
            parent_id=it.next_int(),
            last_fill_price=it.next_float(),
            client_id=it.next_int(),
            why_held=it.next(),
            mkt_cap_price=it.next_float()
        )


@registry.register_message(msg_id=5)
class OpenOrderMessage(IBMessage):
    """Open order message (msg_id=5)."""

    MESSAGE_ID: ClassVar[int] = 5

    order: Order = Field(default_factory=Order)
    contract: Contract = Field(default_factory=Contract)
    order_state: OrderState = Field(default_factory=OrderState)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'OpenOrderMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        order = Order()
        contract = Contract()
        order_state = OrderState()

        # Parse basic order and contract info
        order.orderId = it.next_int()
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

        order.action = it.next()
        order.totalQuantity = it.next_float()
        order.orderType = it.next()
        order.lmtPrice = it.next_float()
        order.auxPrice = it.next_float()
        order.tif = it.next()
        order.ocaGroup = it.next()
        order.account = it.next()
        order.openClose = it.next()
        order.origin = it.next_int()
        order.orderRef = it.next()
        order.clientId = it.next_int()
        order.permId = it.next_int()
        order.outsideRth = it.next_bool()
        order.hidden = it.next_bool()
        order.discretionaryAmt = it.next_float()
        order.goodAfterTime = it.next()
        it.skip(1)  # Skip deprecated field
        order.faGroup = it.next()
        order.faMethod = it.next()
        order.faPercentage = it.next()

        if server_version < 177:
            order.faProfile = it.next()

        order.modelCode = it.next()
        order.goodTillDate = it.next()
        order.rule80A = it.next()
        order.percentOffset = it.next_float()
        order.settlingFirm = it.next()
        order.shortSaleSlot = it.next_int()
        order.designatedLocation = it.next()
        order.exemptCode = it.next_int()
        order.auctionStrategy = it.next_int()
        order.startingPrice = it.next_float()
        order.stockRefPrice = it.next_float()
        order.delta = it.next_float()
        order.stockRangeLower = it.next_float()
        order.stockRangeUpper = it.next_float()
        order.displaySize = it.next_int()
        order.blockOrder = it.next_bool()
        order.sweepToFill = it.next_bool()
        order.allOrNone = it.next_bool()
        order.minQty = it.next_int()
        order.ocaType = it.next_int()
        order.eTradeOnly = it.next_bool()
        order.firmQuoteOnly = it.next_bool()
        order.nbboPriceCap = it.next_float()
        order.parentId = it.next_int()
        order.triggerMethod = it.next_int()
        order.volatility = it.next_float()
        order.volatilityType = it.next_int()
        order.deltaNeutralOrderType = it.next()
        order.deltaNeutralAuxPrice = it.next_float()

        # Parse delta neutral contract if present
        if order.deltaNeutralOrderType:
            order.deltaNeutralConId = it.next_int()
            order.deltaNeutralSettlingFirm = it.next()
            order.deltaNeutralClearingAccount = it.next()
            order.deltaNeutralClearingIntent = it.next()
            order.deltaNeutralOpenClose = it.next()
            order.deltaNeutralShortSale = it.next_bool()
            order.deltaNeutralShortSaleSlot = it.next_int()
            order.deltaNeutralDesignatedLocation = it.next()

        order.continuousUpdate = it.next_bool()
        order.referencePriceType = it.next_int()
        order.trailStopPrice = it.next_float()
        order.trailingPercent = it.next_float()
        order.basisPoints = it.next_float()
        order.basisPointsType = it.next_int()
        contract.comboLegsDescrip = it.next()

        # Parse combo legs
        num_legs = it.next_int()
        contract.comboLegs = []
        for _ in range(num_legs):
            leg = ComboLeg()
            leg.conId = it.next_int()
            leg.ratio = it.next_int()
            leg.action = it.next()
            leg.exchange = it.next()
            leg.openClose = it.next_int()
            leg.shortSaleSlot = it.next_int()
            leg.designatedLocation = it.next()
            leg.exemptCode = it.next_int()
            contract.comboLegs.append(leg)

        # Parse order combo legs
        num_order_legs = it.next_int()
        order.orderComboLegs = []
        for _ in range(num_order_legs):
            leg = OrderComboLeg()
            leg.price = it.next_float()
            order.orderComboLegs.append(leg)

        # Parse smart combo routing params
        num_params = it.next_int()
        if num_params > 0:
            order.smartComboRoutingParams = []
            for _ in range(num_params):
                tag = it.next()
                value = it.next()
                order.smartComboRoutingParams.append(TagValue(tag, value))

        # Parse scale order fields
        order.scaleInitLevelSize = it.next_int()
        order.scaleSubsLevelSize = it.next_int()
        increment = it.next()
        order.scalePriceIncrement = float(increment) if increment else UNSET_DOUBLE

        if 0 < order.scalePriceIncrement < UNSET_DOUBLE:
            order.scalePriceAdjustValue = it.next_float()
            order.scalePriceAdjustInterval = it.next_int()
            order.scaleProfitOffset = it.next_float()
            order.scaleAutoReset = it.next_bool()
            order.scaleInitPosition = it.next_int()
            order.scaleInitFillQty = it.next_int()
            order.scaleRandomPercent = it.next_bool()

        # Parse hedge fields
        order.hedgeType = it.next()
        if order.hedgeType:
            order.hedgeParam = it.next()

        order.optOutSmartRouting = it.next_bool()
        order.clearingAccount = it.next()
        order.clearingIntent = it.next()
        order.notHeld = it.next_bool()

        # Parse delta neutral contract
        dnc_present = it.next_bool()
        if dnc_present:
            con_id = it.next_int()
            delta = it.next_float()
            price = it.next_float()
            contract.deltaNeutralContract = DeltaNeutralContract(con_id, delta, price)

        # Parse algo strategy
        order.algoStrategy = it.next()
        if order.algoStrategy:
            num_algo_params = it.next_int()
            if num_algo_params > 0:
                order.algoParams = []
                for _ in range(num_algo_params):
                    tag = it.next()
                    value = it.next()
                    order.algoParams.append(TagValue(tag, value))

        order.solicited = it.next_bool()
        order.whatIf = it.next_bool()
        order_state.status = it.next()
        order_state.initMarginBefore = it.next()
        order_state.maintMarginBefore = it.next()
        order_state.equityWithLoanBefore = it.next()
        order_state.initMarginChange = it.next()
        order_state.maintMarginChange = it.next()
        order_state.equityWithLoanChange = it.next()
        order_state.initMarginAfter = it.next()
        order_state.maintMarginAfter = it.next()
        order_state.equityWithLoanAfter = it.next()
        order_state.commission = it.next_float()
        order_state.minCommission = it.next_float()
        order_state.maxCommission = it.next_float()
        order_state.commissionCurrency = it.next()
        order_state.warningText = it.next()

        order.randomizeSize = it.next_bool()
        order.randomizePrice = it.next_bool()

        # Parse PEG BENCH fields
        if order.orderType in ('PEG BENCH', 'PEGBENCH'):
            order.referenceContractId = it.next_int()
            order.isPeggedChangeAmountDecrease = it.next_bool()
            order.peggedChangeAmount = it.next_float()
            order.referenceChangeAmount = it.next_float()
            order.referenceExchangeId = it.next()

        # Parse conditions
        num_conditions = it.next_int()
        if num_conditions > 0:
            for _ in range(num_conditions):
                cond_type = it.next_int()
                cond_cls = OrderCondition.createClass(cond_type)
                # Simplified - full implementation would parse all condition fields
                condition = cond_cls(cond_type)
                order.conditions.append(condition)

            order.conditionsIgnoreRth = it.next_bool()
            order.conditionsCancelOrder = it.next_bool()

        # Parse additional fields
        order.adjustedOrderType = it.next()
        order.triggerPrice = it.next_float()
        order.trailStopPrice = it.next_float()
        order.lmtPriceOffset = it.next_float()
        order.adjustedStopPrice = it.next_float()
        order.adjustedStopLimitPrice = it.next_float()
        order.adjustedTrailingAmount = it.next_float()
        order.adjustableTrailingUnit = it.next_int()
        order.softDollarTier.name = it.next()
        order.softDollarTier.val = it.next()
        order.softDollarTier.displayName = it.next()
        order.cashQty = it.next_float()
        order.dontUseAutoPriceForHedge = it.next_bool()
        order.isOmsContainer = it.next_bool()
        order.discretionaryUpToLimitPrice = it.next_bool()
        order.usePriceMgmtAlgo = it.next_bool()

        # Server version specific fields
        if server_version >= 159:
            order.duration = it.next_int()
        if server_version >= 160:
            order.postToAts = it.next_int()
        if server_version >= 162:
            order.autoCancelParent = it.next_bool()
        if server_version >= 170:
            order.minTradeQty = it.next_int()
            order.minCompeteSize = it.next_int()
            order.competeAgainstBestOffset = it.next_float()
            order.midOffsetAtWhole = it.next_float()
            order.midOffsetAtHalf = it.next_float()

        return cls(order=order, contract=contract, order_state=order_state)


@registry.register_message(msg_id=11)
class ExecDetailsMessage(IBMessage):
    """Execution details message (msg_id=11)."""

    MESSAGE_ID: ClassVar[int] = 11

    req_id: int
    contract: Contract = Field(default_factory=Contract)
    execution: Execution = Field(default_factory=Execution)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'ExecDetailsMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        req_id = it.next_int()
        contract = Contract()
        execution = Execution()

        execution.orderId = it.next_int()
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

        execution.execId = it.next()
        time_str = it.next()
        execution.acctNumber = it.next()
        execution.exchange = it.next()
        execution.side = it.next()
        execution.shares = it.next_float()
        execution.price = it.next_float()
        execution.permId = it.next_int()
        execution.clientId = it.next_int()
        execution.liquidation = it.next_int()
        execution.cumQty = it.next_float()
        execution.avgPrice = it.next_float()
        execution.orderRef = it.next()
        execution.evRule = it.next()
        execution.evMultiplier = it.next_float()
        execution.modelCode = it.next()
        execution.lastLiquidity = it.next_int()

        if server_version >= 178:
            execution.pendingPriceRevision = it.next_bool()

        # Parse time
        if time_str:
            execution.time = parseIBDatetime(time_str)

        return cls(req_id=req_id, contract=contract, execution=execution)


@registry.register_message(msg_id=53)
class OpenOrderEndMessage(IBMessage):
    """Open order end message (msg_id=53)."""

    MESSAGE_ID: ClassVar[int] = 53

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'OpenOrderEndMessage':
        """Parse from IB wire format fields."""
        return cls()


@registry.register_message(msg_id=55)
class ExecDetailsEndMessage(IBMessage):
    """Execution details end message (msg_id=55)."""

    MESSAGE_ID: ClassVar[int] = 55

    req_id: int

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'ExecDetailsEndMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        return cls(req_id=it.next_int())


@registry.register_message(msg_id=100)
class OrderBoundMessage(IBMessage):
    """Order bound message (msg_id=100)."""

    MESSAGE_ID: ClassVar[int] = 100

    order_id: int
    api_client_id: int
    api_order_id: int

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'OrderBoundMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(2)  # Skip message ID and version

        return cls(
            order_id=it.next_int(),
            api_client_id=it.next_int(),
            api_order_id=it.next_int()
        )


@registry.register_message(msg_id=101)
class CompletedOrderMessage(IBMessage):
    """Completed order message (msg_id=101)."""

    MESSAGE_ID: ClassVar[int] = 101

    contract: Contract = Field(default_factory=Contract)
    order: Order = Field(default_factory=Order)
    order_state: OrderState = Field(default_factory=OrderState)

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'CompletedOrderMessage':
        """Parse from IB wire format fields."""
        it = FieldIterator(fields)
        it.skip(1)  # Skip message ID

        contract = Contract()
        order = Order()
        order_state = OrderState()

        # Parse contract
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

        # Parse order
        order.action = it.next()
        order.totalQuantity = it.next_float()
        order.orderType = it.next()
        order.lmtPrice = it.next_float()
        order.auxPrice = it.next_float()
        order.tif = it.next()
        order.ocaGroup = it.next()
        order.account = it.next()
        order.openClose = it.next()
        order.origin = it.next_int()
        order.orderRef = it.next()
        order.permId = it.next_int()
        order.outsideRth = it.next_bool()
        order.hidden = it.next_bool()
        order.discretionaryAmt = it.next_float()
        order.goodAfterTime = it.next()
        order.faGroup = it.next()
        order.faMethod = it.next()
        order.faPercentage = it.next()

        if server_version < 177:
            order.faProfile = it.next()

        order.modelCode = it.next()
        order.goodTillDate = it.next()
        order.rule80A = it.next()
        order.percentOffset = it.next_float()
        order.settlingFirm = it.next()
        order.shortSaleSlot = it.next_int()
        order.designatedLocation = it.next()
        order.exemptCode = it.next_int()
        order.startingPrice = it.next_float()
        order.stockRefPrice = it.next_float()
        order.delta = it.next_float()
        order.stockRangeLower = it.next_float()
        order.stockRangeUpper = it.next_float()
        order.displaySize = it.next_int()
        order.sweepToFill = it.next_bool()
        order.allOrNone = it.next_bool()
        order.minQty = it.next_int()
        order.ocaType = it.next_int()
        order.triggerMethod = it.next_int()
        order.volatility = it.next_float()
        order.volatilityType = it.next_int()
        order.deltaNeutralOrderType = it.next()
        order.deltaNeutralAuxPrice = it.next_float()

        # Parse delta neutral fields
        if order.deltaNeutralOrderType:
            order.deltaNeutralConId = it.next_int()
            order.deltaNeutralShortSale = it.next_bool()
            order.deltaNeutralShortSaleSlot = it.next_int()
            order.deltaNeutralDesignatedLocation = it.next()

        order.continuousUpdate = it.next_bool()
        order.referencePriceType = it.next_int()
        order.trailStopPrice = it.next_float()
        order.trailingPercent = it.next_float()
        contract.comboLegsDescrip = it.next()

        # Parse combo legs (simplified)
        num_legs = it.next_int()
        contract.comboLegs = []
        for _ in range(num_legs):
            leg = ComboLeg()
            leg.conId = it.next_int()
            leg.ratio = it.next_int()
            leg.action = it.next()
            leg.exchange = it.next()
            leg.openClose = it.next_int()
            leg.shortSaleSlot = it.next_int()
            leg.designatedLocation = it.next()
            leg.exemptCode = it.next_int()
            contract.comboLegs.append(leg)

        # Parse order combo legs
        num_order_legs = it.next_int()
        order.orderComboLegs = []
        for _ in range(num_order_legs):
            leg = OrderComboLeg()
            leg.price = it.next_float()
            order.orderComboLegs.append(leg)

        # Parse smart combo routing params
        num_params = it.next_int()
        if num_params > 0:
            order.smartComboRoutingParams = []
            for _ in range(num_params):
                tag = it.next()
                value = it.next()
                order.smartComboRoutingParams.append(TagValue(tag, value))

        # Parse scale order fields
        order.scaleInitLevelSize = it.next_int()
        order.scaleSubsLevelSize = it.next_int()
        increment = it.next()
        order.scalePriceIncrement = float(increment) if increment else UNSET_DOUBLE

        if 0 < order.scalePriceIncrement < UNSET_DOUBLE:
            order.scalePriceAdjustValue = it.next_float()
            order.scalePriceAdjustInterval = it.next_int()
            order.scaleProfitOffset = it.next_float()
            order.scaleAutoReset = it.next_bool()
            order.scaleInitPosition = it.next_int()
            order.scaleInitFillQty = it.next_int()
            order.scaleRandomPercent = it.next_bool()

        # Parse hedge fields
        order.hedgeType = it.next()
        if order.hedgeType:
            order.hedgeParam = it.next()

        order.clearingAccount = it.next()
        order.clearingIntent = it.next()
        order.notHeld = it.next_bool()

        # Parse delta neutral contract
        dnc_present = it.next_bool()
        if dnc_present:
            con_id = it.next_int()
            delta = it.next_float()
            price = it.next_float()
            contract.deltaNeutralContract = DeltaNeutralContract(con_id, delta, price)

        # Parse algo strategy
        order.algoStrategy = it.next()
        if order.algoStrategy:
            num_algo_params = it.next_int()
            if num_algo_params > 0:
                order.algoParams = []
                for _ in range(num_algo_params):
                    tag = it.next()
                    value = it.next()
                    order.algoParams.append(TagValue(tag, value))

        order.solicited = it.next_bool()
        order_state.status = it.next()
        order.randomizeSize = it.next_bool()
        order.randomizePrice = it.next_bool()

        # Parse PEG BENCH fields
        if order.orderType in ('PEG BENCH', 'PEGBENCH'):
            order.referenceContractId = it.next_int()
            order.isPeggedChangeAmountDecrease = it.next_bool()
            order.peggedChangeAmount = it.next_float()
            order.referenceChangeAmount = it.next_float()
            order.referenceExchangeId = it.next()

        # Parse conditions (simplified)
        num_conditions = it.next_int()
        if num_conditions > 0:
            for _ in range(num_conditions):
                cond_type = it.next_int()
                cond_cls = OrderCondition.createClass(cond_type)
                condition = cond_cls(cond_type)
                order.conditions.append(condition)

            order.conditionsIgnoreRth = it.next_bool()
            order.conditionsCancelOrder = it.next_bool()

        # Additional fields
        order.trailStopPrice = it.next_float()
        order.lmtPriceOffset = it.next_float()
        order.cashQty = it.next_float()
        order.dontUseAutoPriceForHedge = it.next_bool()
        order.isOmsContainer = it.next_bool()
        order.autoCancelDate = it.next()
        order.filledQuantity = it.next_float()
        order.refFuturesConId = it.next_int()
        order.autoCancelParent = it.next_bool()
        order.shareholder = it.next()
        order.imbalanceOnly = it.next_bool()
        order.routeMarketableToBbo = it.next_bool()
        order.parentPermId = it.next_int()
        order_state.completedTime = it.next()
        order_state.completedStatus = it.next()

        if server_version >= 170:
            order.minTradeQty = it.next_int()
            order.minCompeteSize = it.next_int()
            order.competeAgainstBestOffset = it.next_float()
            order.midOffsetAtWhole = it.next_float()
            order.midOffsetAtHalf = it.next_float()

        return cls(contract=contract, order=order, order_state=order_state)


@registry.register_message(msg_id=102)
class CompletedOrdersEndMessage(IBMessage):
    """Completed orders end message (msg_id=102)."""

    MESSAGE_ID: ClassVar[int] = 102

    @classmethod
    def from_fields(cls, fields: list[str], server_version: int = 0) -> 'CompletedOrdersEndMessage':
        """Parse from IB wire format fields."""
        return cls()
