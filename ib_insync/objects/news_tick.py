"""NewsTick NamedTuple."""

from typing import NamedTuple


class NewsTick(NamedTuple):
    timeStamp: int
    providerCode: str
    articleId: str
    headline: str
    extraData: str
