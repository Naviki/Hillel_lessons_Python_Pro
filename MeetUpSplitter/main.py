import uuid
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from auth.database import User, get_async_session
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from meeting.crud import get_meeting, update_meeting, delete_meeting, add_participant_to_meeting, \
    check_user_participation, get_meeting_participants
from meeting.schemas import Meeting, MeetingCreate, MeetingUpdate, Comment, CommentCreate, CommentUpdate, \
    MeetingParticipant, Purchase, PurchaseCreate

app = FastAPI(
    title='MeetUpSplitter App'
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, anonym"


@app.post("/meetings/", response_model=Meeting)
async def create_meeting(meeting_create: MeetingCreate, user: User = Depends(current_user)):
    async with get_async_session() as session:
        meeting_id = create_meeting(session, meeting_create, user.id)
        if meeting_id:
            return meeting_id
        else:
            raise HTTPException(status_code=500, detail="Meeting creation failed")


@app.get("/meetings/", response_model=List[Meeting])
async def get_meetings(skip: int = 0, limit: int = 10):
    return get_meetings(get_async_session(), skip, limit)


@app.get("/meetings/{meeting_id}", response_model=Meeting)
async def get_single_meeting(meeting_id: uuid.UUID):
    async with get_async_session() as session:
        result = get_meeting(session, meeting_id)
        if not result:
            raise HTTPException(status_code=404, detail="Meeting not found")
        return result


@app.put("/meetings/{meeting_id}", response_model=Meeting)
async def update_single_meeting(meeting_id: uuid.UUID, meeting_update: MeetingUpdate):
    async with get_async_session() as session:
        result = update_meeting(session, meeting_id, meeting_update)
        if not result:
            raise HTTPException(status_code=404, detail="Meeting not found")
        return result


@app.delete("/meetings/{meeting_id}")
async def delete_single_meeting(meeting_id: uuid.UUID):
    async with get_async_session() as session:
        result = delete_meeting(session, meeting_id)
        if not result:
            raise HTTPException(status_code=404, detail="Meeting not found")
        return {"message": "Meeting deleted successfully"}


@app.post("/meetings/{meeting_id}/participants/", response_model=Meeting)
async def add_participant(meeting_id: uuid.UUID, user_id: uuid.UUID):
    async with get_async_session() as session:
        result = add_participant_to_meeting(session, meeting_id, user_id)
        if not result:
            raise HTTPException(status_code=404, detail="Meeting or user not found")
        return result


@app.post("/meetings/{meeting_id}/comments/", response_model=Comment)
async def create_comment(meeting_id: uuid.UUID, comment_create: CommentCreate, user: User = Depends(current_user)):
    result = create_comment(get_async_session(), meeting_id, user.id, comment_create.content)
    if not result:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return result


@app.put("/meetings/{meeting_id}/comments/{comment_id}", response_model=Comment)
async def update_comment(comment_id: uuid.UUID, comment_update: CommentUpdate):
    result = update_comment(get_async_session(), comment_id, comment_update.content)
    if not result:
        raise HTTPException(status_code=404, detail="Comment not found")
    return result


@app.delete("/meetings/{meeting_id}/comments/{comment_id}")
async def delete_comment(comment_id: uuid.UUID):
    result = delete_comment(get_async_session(), comment_id)
    if not result:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}


@app.get("/meetings/", response_model=List[Meeting])
async def list_meetings(
    skip: int = 0,
    limit: int = 10,
):
    meetings = get_meetings(get_async_session(), skip=skip, limit=limit)
    return meetings


@app.post("/meetings/{meeting_id}/join/", response_model=MeetingParticipant)
async def join_meeting(meeting_id: uuid.UUID, user: User = Depends(current_user)):
    async with get_async_session() as session:
        meeting = get_meeting(session, meeting_id)
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")

        participant = add_participant_to_meeting(session, meeting_id, user.id)
        return participant


@app.post("/meetings/{meeting_id}/purchases/", response_model=Purchase)
async def create_purchase(
    meeting_id: uuid.UUID,
    purchase_create: PurchaseCreate,
    user: User = Depends(current_user)
):
    async with get_async_session() as session:
        is_participant = await check_user_participation(session, meeting_id, user.id)
        if not is_participant:
            raise HTTPException(status_code=403, detail="You are not a participant of this meeting")

        result = await create_purchase(session, meeting_id, purchase_create, user.id)
        if not result:
            raise HTTPException(status_code=404, detail="Meeting not found")
        return result


@app.get("/meetings/{meeting_id}", response_model=Meeting)
async def read_meeting(meeting_id: uuid.UUID):
    async with get_async_session() as session:
        meeting = get_meeting(session, meeting_id)
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")

        participants = get_meeting_participants(session, meeting_id)
        meeting.participants = participants

        return meeting
