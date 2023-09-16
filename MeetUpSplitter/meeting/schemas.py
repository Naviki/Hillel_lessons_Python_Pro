from pydantic import BaseModel
from datetime import datetime
from typing import List
import uuid


class MeetingBase(BaseModel):
    place: str
    time: datetime
    participants: List[uuid.UUID]


class MeetingCreate(MeetingBase):
    pass


class Meeting(MeetingBase):
    id: uuid.UUID


class MeetingUpdate(MeetingBase):
    pass


class MeetingParticipantBase(BaseModel):
    user_id: uuid.UUID


class MeetingParticipantCreate(MeetingParticipantBase):
    pass


class MeetingParticipant(MeetingParticipantBase):
    id: uuid.UUID
    meeting_id: uuid.UUID


class MeetingParticipantUpdate(MeetingParticipantBase):
    pass


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: uuid.UUID
    meeting_id: uuid.UUID
    user_id: uuid.UUID


class CommentUpdate(CommentBase):
    pass


class PurchaseBase(BaseModel):
    description: str
    amount: float


class PurchaseCreate(PurchaseBase):
    pass


class Purchase(PurchaseBase):
    id: uuid.UUID


class PurchaseUpdate(PurchaseBase):
    pass
