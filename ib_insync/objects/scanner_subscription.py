"""ScannerSubscription dataclass."""

from dataclasses import dataclass

from ..util import UNSET_DOUBLE, UNSET_INTEGER


@dataclass
class ScannerSubscription:
    numberOfRows: int = -1
    instrument: str = ''
    locationCode: str = ''
    scanCode: str = ''
    abovePrice: float = UNSET_DOUBLE
    belowPrice: float = UNSET_DOUBLE
    aboveVolume: int = UNSET_INTEGER
    marketCapAbove: float = UNSET_DOUBLE
    marketCapBelow: float = UNSET_DOUBLE
    moodyRatingAbove: str = ''
    moodyRatingBelow: str = ''
    spRatingAbove: str = ''
    spRatingBelow: str = ''
    maturityDateAbove: str = ''
    maturityDateBelow: str = ''
    couponRateAbove: float = UNSET_DOUBLE
    couponRateBelow: float = UNSET_DOUBLE
    excludeConvertible: bool = False
    averageOptionVolumeAbove: int = UNSET_INTEGER
    scannerSettingPairs: str = ''
    stockTypeFilter: str = ''
