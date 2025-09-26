"""PortfolioItem NamedTuple."""

from typing import NamedTuple

from ..contract import Contract


class PortfolioItem(NamedTuple):
    contract: Contract
    position: float
    marketPrice: float
    marketValue: float
    averageCost: float
    unrealizedPNL: float
    realizedPNL: float
    account: str
