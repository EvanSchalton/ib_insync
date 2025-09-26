"""Event topics for the ib_insync event system."""

from enum import Enum


class EventTopic(str, Enum):
    """Event topics used throughout the ib_insync system."""

    # Connection events
    CONNECTED = "connectedEvent"
    DISCONNECTED = "disconnectedEvent"
    API_START = "apiStart"
    API_END = "apiEnd"
    API_ERROR = "apiError"
    HAS_DATA = "hasData"

    # Throttling events
    THROTTLE_START = "throttleStart"
    THROTTLE_END = "throttleEnd"

    # General update events
    UPDATE = "updateEvent"
    PENDING_TICKERS = "pendingTickersEvent"
    BAR_UPDATE = "barUpdateEvent"

    # Order events
    NEW_ORDER = "newOrderEvent"
    ORDER_MODIFY = "orderModifyEvent"
    CANCEL_ORDER = "cancelOrderEvent"
    OPEN_ORDER = "openOrderEvent"
    ORDER_STATUS = "orderStatusEvent"

    # Order-specific events (for Trade objects)
    STATUS = "statusEvent"
    MODIFY = "modifyEvent"
    FILL = "fillEvent"
    FILLED = "filledEvent"
    CANCEL = "cancelEvent"
    CANCELLED = "cancelledEvent"

    # Execution events
    EXEC_DETAILS = "execDetailsEvent"
    COMMISSION_REPORT = "commissionReportEvent"

    # Portfolio events
    UPDATE_PORTFOLIO = "updatePortfolioEvent"
    POSITION = "positionEvent"

    # Account events
    ACCOUNT_VALUE = "accountValueEvent"
    ACCOUNT_SUMMARY = "accountSummaryEvent"
    PNL = "pnlEvent"
    PNL_SINGLE = "pnlSingleEvent"

    # Market data events
    SCANNER_DATA = "scannerDataEvent"
    TICK_NEWS = "tickNewsEvent"
    NEWS_BULLETIN = "newsBulletinEvent"

    # Wall Street Horizon events
    WSH_META = "wshMetaEvent"
    WSH = "wshEvent"

    # Error and timeout events
    ERROR = "errorEvent"
    TIMEOUT = "timeoutEvent"

    # IB Controller events
    STARTING = "startingEvent"
    STARTED = "startedEvent"
    STOPPING = "stoppingEvent"
    STOPPED = "stoppedEvent"
    SOFT_TIMEOUT = "softTimeoutEvent"
    HARD_TIMEOUT = "hardTimeoutEvent"
