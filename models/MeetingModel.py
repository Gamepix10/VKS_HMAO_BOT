from datetime import datetime
import pydantic


class MeetingModel(pydantic.BaseModel):
    permalinkId: str
    permalink: str
    id: int
    name: str
    roomId: int
    participantsCount: int
    sendNotificationsAt: datetime
    startedAt: datetime
    endedAt: datetime
    duration: int
    isGovernorPresents: bool
    createdAt: datetime
    closedAt: datetime
    state: str
    organizedBy: int
    createdBy: int
    isNotifyAccepted: bool
    isVirtual: bool
    organizerPermalinkId: str
    organizerPermalink: str
    comment: str

    class Event(pydantic.BaseModel):
        isOfflineEvent: bool
        roomId: int
        name: str
        startedAt: datetime
        endedAt: datetime
        duration: int
        id: int

    class Room(pydantic.BaseModel):
        name: str
        description: str
        id: int
        buildingId: int
        maxParticipants: int
        isSkitNotified: bool

        class ResponsibleUser(pydantic.BaseModel):
            id: int
            lastName: str
            firstName: str
            middleName: str
            roleIds: list[int]
            departmentId: int
            email: str

        responsibleUser: ResponsibleUser

    class CiscoRoom(pydantic.BaseModel):
        connectUrl: str
        roomUri: str
        sipDomainUrl: str
        sipIpUrl: str
        callId: str
        id: int
        adminConnectUrl: str
        adminAccessUri: str

    class CiscoSettings(pydantic.BaseModel):
        isMicrophoneOn: bool
        isVideoOn: bool
        isWaitingRoomEnabled: bool
        needVideoRecording: bool
        id: int
        isPrivateLicenceUsed: bool

    class VinteoRoom(pydantic.BaseModel):
        id: int
        callId: str
        connectUrl: str
        connectCode: int
        sipDomainUrl: str
        sipIpUrl: str
        organizerNumber: int
        organizerPassword: str

    class VinteoSettings(pydantic.BaseModel):
        id: int
        needVideoRecording: bool

    class ExternalSettings(pydantic.BaseModel):
        externalUrl: str
        permanentRoomId: int
        id: int

        class PermanentRoom(pydantic.BaseModel):
            name: str
            description: str
            id: int
            link: str
            backend: str
            createdAt: datetime

        permanentRoom: PermanentRoom

    class Participant(pydantic.BaseModel):
        id: int
        email: str
        lastName: str
        firstName: str
        middleName: str
        isApproved: bool

    class Attachment(pydantic.BaseModel):
        name: str
        id: str

    class Group(pydantic.BaseModel):
        id: int
        name: str
        description: str
        params: dict
        isPublic: bool
        copiedFromId: int
        membersCount: int
        createdBy: int

    class CreatedUser(pydantic.BaseModel):
        id: int
        lastName: str
        firstName: str
        middleName: str
        roleIds: list[int]
        departmentId: int
        email: str

    class OrganizedUser(pydantic.BaseModel):
        id: int
        lastName: str
        firstName: str
        middleName: str
        roleIds: list[int]
        departmentId: int
        email: str

    class Recurrence(pydantic.BaseModel):
        frequency: int
        startedAt: datetime
        interval: int
        count: int
        until: datetime
        weekDays: list[int]
        additionalDates: list[datetime]
        excludeDates: list[datetime]
        id: int

    event: Event
    room: Room
    ciscoRoom: CiscoRoom
    ciscoSettings: CiscoSettings
    vinteoRoom: VinteoRoom
    vinteoSettings: VinteoSettings
    externalSettings: ExternalSettings
    participants: list[Participant]
    attachments: list[Attachment]
    groups: list[Group]
    ciscoSettingsId: int
    ciscoRoomId: int
    eventId: int
    updatedAt: datetime
    backend: str
    createdUser: CreatedUser
    organizedUser: OrganizedUser
    recurrence: Recurrence
