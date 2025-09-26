"""PnL dataclass."""

from dataclasses import dataclass

nan = float('nan')


@dataclass
class PnL:
    account: str = ''
    modelCode: str = ''
    dailyPnL: float = nan
    unrealizedPnL: float = nan
    realizedPnL: float = nan
