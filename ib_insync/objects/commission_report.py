"""CommissionReport dataclass."""

from dataclasses import dataclass


@dataclass
class CommissionReport:
    execId: str = ''
    commission: float = 0.0
    currency: str = ''
    realizedPNL: float = 0.0
    yield_: float = 0.0
    yieldRedemptionDate: int = 0
