"""BarDataList custom class."""

from datetime import date as date_
from datetime import datetime

from eventkit import Event

from ..contract import Contract, TagValue
from ..event_topic import EventTopic
from .bar_data import BarData


class BarDataList(list[BarData]):
    """
    List of :class:`.BarData` that also stores all request parameters.

    Events:

        * ``updateEvent``
          (bars: :class:`.BarDataList`, hasNewBar: bool)
    """

    reqId: int
    contract: Contract
    endDateTime: datetime | date_ | str | None
    durationStr: str
    barSizeSetting: str
    whatToShow: str
    useRTH: bool
    formatDate: int
    keepUpToDate: bool
    chartOptions: list[TagValue]

    def __init__(self, *args):
        super().__init__(*args)
        self.updateEvent = Event(EventTopic.UPDATE)

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return id(self)
