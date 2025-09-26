"""Improved enumerations for IB contract types."""

from enum import Enum


class SecurityType(str, Enum):
    """Security types supported by Interactive Brokers."""

    STOCK = "STK"
    OPTION = "OPT"
    FUTURE = "FUT"
    CONTINUOUS_FUTURE = "CONTFUT"
    FOREX = "CASH"
    INDEX = "IND"
    CFD = "CFD"
    BOND = "BOND"
    COMMODITY = "CMDTY"
    FUTURES_OPTION = "FOP"
    FUND = "FUND"
    WARRANT = "WAR"
    WARRANT_OPTION = "IOPT"
    COMBO = "BAG"
    CRYPTO = "CRYPTO"
    NEWS = "NEWS"
    EVENT = "EVENT"


class OptionType(str, Enum):
    """Option types (formerly Right)."""

    CALL = "C"
    PUT = "P"

    @classmethod
    def from_string(cls, value: str) -> "OptionType":
        """Convert various string formats to OptionType."""
        if not value:
            return None
        value = value.upper()
        if value in ("C", "CALL"):
            return cls.CALL
        elif value in ("P", "PUT"):
            return cls.PUT
        else:
            raise ValueError(f"Invalid option type: {value}")


class OrderAction(str, Enum):
    """Order actions."""

    BUY = "BUY"
    SELL = "SELL"


class Exchange(str, Enum):
    """Major exchanges supported by IB."""

    # Smart routing
    SMART = "SMART"

    # US Stock Exchanges
    NYSE = "NYSE"
    NASDAQ = "NASDAQ"
    AMEX = "AMEX"
    ARCA = "ARCA"
    ISLAND = "ISLAND"
    BATS = "BATS"
    IEX = "IEX"
    EDGEA = "EDGEA"
    BYX = "BYX"

    # US Options Exchanges
    CBOE = "CBOE"
    ISE = "ISE"
    PHLX = "PHLX"
    BOX = "BOX"

    # US Futures Exchanges
    GLOBEX = "GLOBEX"
    ECBOT = "ECBOT"
    NYMEX = "NYMEX"
    COMEX = "COMEX"
    CBOT = "CBOT"
    ICE = "ICE"
    CFE = "CFE"
    NYBOT = "NYBOT"

    # European Exchanges
    IBIS = "IBIS"  # Germany
    LSE = "LSE"    # London
    SBF = "SBF"    # Paris
    AEB = "AEB"    # Amsterdam
    BVME = "BVME"  # Milan
    IBIS2 = "IBIS2"
    FWB = "FWB"    # Frankfurt
    SWB = "SWB"    # Stuttgart
    BATEEN = "BATEEN"

    # Asian Exchanges
    SEHK = "SEHK"      # Hong Kong
    HKFE = "HKFE"      # Hong Kong Futures
    TSE = "TSE"        # Tokyo
    OSE = "OSE.JPN"    # Osaka
    SGX = "SGX"        # Singapore
    NSE = "NSE"        # India

    # Other Exchanges
    ASX = "ASX"        # Australia
    SNFE = "SNFE"      # Sydney Futures
    TSX = "TSX"        # Toronto
    VENTURE = "VENTURE" # TSX Venture
    MX = "MX"          # Montreal

    # Forex
    IDEALPRO = "IDEALPRO"
    FXCONV = "FXCONV"

    # Crypto
    PAXOS = "PAXOS"

    @classmethod
    def _missing_(cls, value):
        """Allow any string as exchange for flexibility."""
        # For exchanges not in our enum, return None to keep as string
        # This allows IB to add new exchanges without breaking our code
        return None


class Currency(str, Enum):
    """Major currencies supported by IB."""

    # Major Currencies
    USD = "USD"  # US Dollar
    EUR = "EUR"  # Euro
    GBP = "GBP"  # British Pound
    JPY = "JPY"  # Japanese Yen
    CHF = "CHF"  # Swiss Franc
    CAD = "CAD"  # Canadian Dollar
    AUD = "AUD"  # Australian Dollar
    NZD = "NZD"  # New Zealand Dollar

    # Asian Currencies
    CNH = "CNH"  # Chinese Yuan (offshore)
    CNY = "CNY"  # Chinese Yuan (onshore)
    HKD = "HKD"  # Hong Kong Dollar
    SGD = "SGD"  # Singapore Dollar
    KRW = "KRW"  # Korean Won
    INR = "INR"  # Indian Rupee
    THB = "THB"  # Thai Baht
    MYR = "MYR"  # Malaysian Ringgit
    IDR = "IDR"  # Indonesian Rupiah
    PHP = "PHP"  # Philippine Peso
    TWD = "TWD"  # Taiwan Dollar

    # European Currencies (non-Euro)
    SEK = "SEK"  # Swedish Krona
    NOK = "NOK"  # Norwegian Krone
    DKK = "DKK"  # Danish Krone
    PLN = "PLN"  # Polish Zloty
    CZK = "CZK"  # Czech Koruna
    HUF = "HUF"  # Hungarian Forint
    RON = "RON"  # Romanian Leu
    RUB = "RUB"  # Russian Ruble
    TRY = "TRY"  # Turkish Lira

    # Middle East & Africa
    ILS = "ILS"  # Israeli Shekel
    ZAR = "ZAR"  # South African Rand
    AED = "AED"  # UAE Dirham
    SAR = "SAR"  # Saudi Riyal

    # Americas (non-USD)
    MXN = "MXN"  # Mexican Peso
    BRL = "BRL"  # Brazilian Real
    ARS = "ARS"  # Argentine Peso
    CLP = "CLP"  # Chilean Peso
    COP = "COP"  # Colombian Peso
    PEN = "PEN"  # Peruvian Sol

    @classmethod
    def _missing_(cls, value):
        """Allow any string as currency for flexibility."""
        # For currencies not in our enum, return None to keep as string
        # This allows for new currencies without breaking our code
        return None


class SecurityIdType(str, Enum):
    """Security identifier types."""

    ISIN = "ISIN"
    CUSIP = "CUSIP"
    SEDOL = "SEDOL"
    RIC = "RIC"
    FIGI = "FIGI"


class OpenClose(int, Enum):
    """Open/Close status for combo legs."""

    SAME = 0  # Same as the parent order
    OPEN = 1  # Opening position
    CLOSE = 2  # Closing position
    UNKNOWN = 3  # Unknown


class ShortSaleSlot(int, Enum):
    """Short sale slot designation."""

    DEFAULT = 0  # No short sale slot designation
    CLEARING_BROKER = 1  # Shares will be delivered from clearing broker
    THIRD_PARTY = 2  # Shares will be delivered from a third party


class ExemptCode(int, Enum):
    """Short sale exemption codes."""

    APPLIES_UPTICK_RULE = -1  # Applies the short sale uptick rule
    NO_RULE = 0  # Does not apply the rule (exempt)


class LogLevel(int, Enum):
    """TWS/Gateway log levels."""

    SYSTEM = 1
    ERROR = 2
    WARNING = 3
    INFORMATION = 4
    DETAIL = 5
