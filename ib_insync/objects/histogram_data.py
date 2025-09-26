"""HistogramData dataclass."""

from dataclasses import dataclass


@dataclass
class HistogramData:
    price: float = 0.0
    count: int = 0
