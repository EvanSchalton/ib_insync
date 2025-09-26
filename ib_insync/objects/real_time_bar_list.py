"""RealTimeBarList custom class."""


from eventkit import Event

from ..contract import Contract, TagValue
from ..event_topic import EventTopic
from .real_time_bar import RealTimeBar


class RealTimeBarList(list[RealTimeBar]):
    """
    List of :class:`.RealTimeBar` that also stores all request parameters.

    Events:

        * ``updateEvent``
          (bars: :class:`.RealTimeBarList`, hasNewBar: bool)
    """

    reqId: int
    contract: Contract
    barSize: int
    whatToShow: str
    useRTH: bool
    realTimeBarsOptions: list[TagValue]

    def __init__(self, *args):
        super().__init__(*args)
        self.updateEvent = Event(EventTopic.UPDATE)

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return id(self)
