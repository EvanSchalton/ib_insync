"""AccountValue NamedTuple."""

from typing import NamedTuple


class AccountValue(NamedTuple):
    account: str
    tag: str
    value: str
    currency: str
    modelCode: str
