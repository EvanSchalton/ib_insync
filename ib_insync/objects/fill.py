"""Fill NamedTuple."""

from datetime import datetime
from typing import NamedTuple

from ..contract import Contract
from .commission_report import CommissionReport
from .execution import Execution


class Fill(NamedTuple):
    contract: Contract
    execution: Execution
    commissionReport: CommissionReport
    time: datetime
