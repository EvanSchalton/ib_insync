"""Dividends NamedTuple."""

from datetime import date as date_
from typing import NamedTuple


class Dividends(NamedTuple):
    past12Months: float | None
    next12Months: float | None
    nextDate: date_ | None
    nextAmount: float | None
