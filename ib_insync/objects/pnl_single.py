"""PnLSingle dataclass."""

from dataclasses import dataclass

nan = float('nan')


@dataclass
class PnLSingle:
    account: str = ''
    modelCode: str = ''
    conId: int = 0
    dailyPnL: float = nan
    unrealizedPnL: float = nan
    realizedPnL: float = nan
    position: int = 0
    value: float = nan
