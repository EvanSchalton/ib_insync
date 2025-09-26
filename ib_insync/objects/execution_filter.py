"""ExecutionFilter dataclass."""

from dataclasses import dataclass


@dataclass
class ExecutionFilter:
    clientId: int = 0
    acctCode: str = ''
    time: str = ''
    symbol: str = ''
    secType: str = ''
    exchange: str = ''
    side: str = ''
