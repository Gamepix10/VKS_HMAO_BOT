import pydantic
from datetime import datetime
from typing import List
from models.MeetingStateModel import MeetingStateModel

class GetMeetingsModel(pydantic.BaseModel):
    from_datetime: datetime
    to_datetime: datetime
    priority: int
    building_id: int
    room_id: int
    page: int
    backend: str
    sort_by: str
    state: List[MeetingStateModel]

