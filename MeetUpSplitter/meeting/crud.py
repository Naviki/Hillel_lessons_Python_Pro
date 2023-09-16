import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from models.models import meeting, meeting_participant, comment, purchase
from meeting.schemas import MeetingCreate, MeetingUpdate, PurchaseCreate, Purchase


def create_meeting(db: Session, meeting: MeetingCreate, user_id: uuid.UUID):
    db_meeting = meeting.insert().values(
        place=meeting.place,
        time=meeting.time,
        user_id=user_id
    )
    db.execute(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting


def get_meetings(db: Session, skip: int = 0, limit: int = 10):
    return db.execute(meeting.select().offset(skip).limit(limit)).fetchall()


def get_meeting(db: Session, meeting_id: uuid.UUID):
    return db.execute(meeting.select().where(meeting.c.id == meeting_id)).fetchone()


def update_meeting(db: Session, meeting_id: uuid.UUID, meeting_update: MeetingUpdate):
    db_meeting = meeting.update().where(meeting.c.id == meeting_id).values(**meeting_update.model_dump())
    db.execute(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting


def delete_meeting(db: Session, meeting_id: uuid.UUID):
    db_meeting = meeting.delete().where(meeting.c.id == meeting_id)
    db.execute(db_meeting)
    db.commit()


def add_participant_to_meeting(db: Session, meeting_id: uuid.UUID, user_id: uuid.UUID):
    db_participant = meeting_participant.insert().values(
        meeting_id=meeting_id,
        user_id=user_id
    )
    db.execute(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant


def create_comment(db: Session, meeting_id: uuid.UUID, user_id: uuid.UUID, content: str):
    db_comment = comment.insert().values(
        meeting_id=meeting_id,
        user_id=user_id,
        content=content
    )
    db.execute(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def update_comment(db: Session, comment_id: uuid.UUID, content: str):
    db_comment = comment.update().where(comment.c.id == comment_id).values(content=content)
    db.execute(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: uuid.UUID):
    db_comment = comment.delete().where(comment.c.id == comment_id)
    db.execute(db_comment)
    db.commit()


async def create_purchase(session: AsyncSession, meeting_id: uuid.UUID, purchase_create: PurchaseCreate):
    async with session.begin():
        purchase_record = purchase.insert().values(
            meeting_id=meeting_id,
            description=purchase_create.description,
            amount=purchase_create.amount,
        )
        result = await session.execute(purchase_record)
        purchase_id = result.scalars().first()
        participant_records = await session.execute(
            meeting_participant.select().where(meeting_participant.c.meeting_id == meeting_id)
        )
        participants = [dict(record) for record in participant_records]
        total_amount = purchase_create.amount
        share_amount = total_amount / len(participants)

        for participant in participants:
            share_record = meeting_participant.update().where(
                meeting_participant.c.id == participant['id']
            ).values(
                share_amount=share_amount
            )
            await session.execute(share_record)

        return Purchase(id=purchase_id, **purchase_create.model_dump())


async def check_user_participation(session: AsyncSession, meeting_id: uuid.UUID, user_id: uuid.UUID):
    participant_record = await session.execute(
        meeting_participant.select().where(
            (meeting_participant.c.meeting_id == meeting_id) &
            (meeting_participant.c.user_id == user_id)
        )
    )
    return participant_record.scalar() is not None


async def get_meeting_participants(session: AsyncSession, meeting_id: uuid.UUID):
    participant_records = await session.execute(
        meeting_participant.select().where(meeting_participant.c.meeting_id == meeting_id)
    )
    participants = [dict(record) for record in participant_records]
    return participants

