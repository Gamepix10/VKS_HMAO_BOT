from enum import Enum


class MeetingStateModel(Enum):
    BOOKED = "booked"
    CANCELLED = "cancelled"
    STARTED = "started"
    ENDED = "ended"

