"""ConnectionStats NamedTuple."""

from typing import NamedTuple


class ConnectionStats(NamedTuple):
    startTime: float
    duration: float
    numBytesRecv: int
    numBytesSent: int
    numMsgRecv: int
    numMsgSent: int
