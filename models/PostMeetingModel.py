from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from models.MeetingStateModel import MeetingStateModel

class PostMeetingModel(BaseModel):
    attachments: List[str]
    name: str
    roomId: int
    comment: str
    participantsCount: int
    sendNotificationsAt: datetime
    ciscoSettings: Optional["CiscoSettings"]
    vinteoSettings: Optional["VinteoSettings"]
    externalSettings: Optional["ExternalSettings"]
    startedAt: datetime
    endedAt: datetime
    duration: int
    isGovernorPresents: bool
    isNotifyAccepted: bool
    participants: List["Participant"]
    groups: List["Group"]
    recurrence: Optional["Recurrence"]
    recurrenceUpdateType: str
    isVirtual: bool
    state: MeetingStateModel
    backend: str
    organizedBy: "OrganizedBy"

    class CiscoSettings(BaseModel):
        isMicrophoneOn: bool
        isVideoOn: bool
        isWaitingRoomEnabled: bool
        needVideoRecording: bool

    class VinteoSettings(BaseModel):
        needVideoRecording: bool

    class ExternalSettings(BaseModel):
        externalUrl: str
        permanentRoomId: int

    class Participant(BaseModel):
        id: int
        email: str
        lastName: str
        firstName: str
        middleName: str

    class Group(BaseModel):
        id: int

    class Recurrence(BaseModel):
        frequency: int
        startedAt: datetime
        interval: int
        count: int
        until: datetime
        weekDays: List[int]
        additionalDates: List[datetime]
        excludeDates: List[datetime]

    class OrganizedBy(BaseModel):
        id: int
