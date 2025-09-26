"""DepthMktDataDescription dataclass."""

from dataclasses import dataclass

from ..util import UNSET_INTEGER


@dataclass
class DepthMktDataDescription:
    exchange: str = ''
    secType: str = ''
    listingExch: str = ''
    serviceDataType: str = ''
    aggGroup: int = UNSET_INTEGER
