"""Execution dataclass."""

from dataclasses import dataclass, field
from datetime import datetime

from ..util import EPOCH


@dataclass
class Execution:
    execId: str = ''
    time: datetime = field(default=EPOCH)
    acctNumber: str = ''
    exchange: str = ''
    side: str = ''
    shares: float = 0.0
    price: float = 0.0
    permId: int = 0
    clientId: int = 0
    orderId: int = 0
    liquidation: int = 0
    cumQty: float = 0.0
    avgPrice: float = 0.0
    orderRef: str = ''
    evRule: str = ''
    evMultiplier: float = 0.0
    modelCode: str = ''
    lastLiquidity: int = 0
    pendingPriceRevision: bool = False
