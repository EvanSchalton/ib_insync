"""ScanDataList custom class."""


from eventkit import Event

from ..contract import ScanData, TagValue
from ..event_topic import EventTopic
from .scanner_subscription import ScannerSubscription


class ScanDataList(list[ScanData]):
    """
    List of :class:`.ScanData` that also stores all request parameters.

    Events:
        * ``updateEvent`` (:class:`.ScanDataList`)
    """

    reqId: int
    subscription: ScannerSubscription
    scannerSubscriptionOptions: list[TagValue]
    scannerSubscriptionFilterOptions: list[TagValue]

    def __init__(self, *args):
        super().__init__(*args)
        self.updateEvent = Event(EventTopic.UPDATE)

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return id(self)
