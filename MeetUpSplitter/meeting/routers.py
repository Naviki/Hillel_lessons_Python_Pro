import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import MeetingCreate, Meeting, CommentCreate, Comment
from crud import create_meeting, get_meetings, get_meeting, add_participant_to_meeting, create_comment
from auth.database import User, get_async_session, current_user

router = APIRouter()


@router.post("/meetings/", response_model=Meeting)
async def create_meeting_endpoint(meeting_create: MeetingCreate, user: User = Depends(current_user), db: Session = Depends(get_async_session)):
    meeting = create_meeting(db, meeting_create, user.id)
    if not meeting:
        raise HTTPException(status_code=500, detail="Meeting creation failed")
    return meeting


@router.get("/meetings/", response_model=List[Meeting])
async def get_meetings_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_async_session)):
    meetings = get_meetings(db, skip, limit)
    return meetings


@router.get("/meetings/{meeting_id}", response_model=Meeting)
async def get_single_meeting_endpoint(meeting_id: uuid.UUID, db: Session = Depends(get_async_session)):
    meeting = get_meeting(db, meeting_id)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@router.post("/meetings/{meeting_id}/add-participant/{user_id}", response_model=Meeting)
async def add_participant_endpoint(meeting_id: uuid.UUID, user_id: uuid.UUID, db: Session = Depends(get_async_session)):
    result = add_participant_to_meeting(db, meeting_id, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Meeting or user not found")
    return result


@router.post("/meetings/{meeting_id}/comments/", response_model=Comment)
async def create_comment_endpoint(meeting_id: uuid.UUID, comment_create: CommentCreate, user: User = Depends(current_user), db: Session = Depends(get_async_session)):
    comment = create_comment(db, meeting_id, user.id, comment_create)
    if not comment:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return comment
