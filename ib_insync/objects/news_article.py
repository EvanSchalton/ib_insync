"""NewsArticle NamedTuple."""

from typing import NamedTuple


class NewsArticle(NamedTuple):
    articleType: int
    articleText: str
