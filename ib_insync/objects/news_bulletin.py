"""NewsBulletin NamedTuple."""

from typing import NamedTuple


class NewsBulletin(NamedTuple):
    msgId: int
    msgType: int
    message: str
    origExchange: str
