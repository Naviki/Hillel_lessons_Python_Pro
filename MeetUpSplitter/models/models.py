from sqlalchemy import MetaData, Table, Column, String, TIMESTAMP, ForeignKey, DateTime, Float, Boolean, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID

from datetime import datetime
import uuid

metadate = MetaData()

role = Table(
    'role',
    metadate,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

user = Table(
    'user',
    metadate,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('email', String(length=255), unique=True, nullable=False),
    Column('username', String(length=255), unique=True, nullable=False),
    Column('hashed_password', String(length=255), nullable=False),
    Column('registered_at', TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)


meeting = Table(
    'meeting',
    metadate,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('place', String(length=255), nullable=False),
    Column('time', DateTime),
    Column('user_id', UUID(as_uuid=True), ForeignKey('user.id'), nullable=False),
)

meeting_participant = Table(
    'meeting_participant',
    metadate,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('meeting_id', UUID(as_uuid=True), ForeignKey('meeting.id'), nullable=False),
    Column('user_id', UUID(as_uuid=True), ForeignKey('user.id'), nullable=False),
)

purchase = Table(
    'purchase',
    metadate,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('meeting_id', UUID(as_uuid=True), ForeignKey('meeting.id'), nullable=False),
    Column('description', String(length=255), nullable=False),
    Column('amount', Float, nullable=False),
)

expense_share = Table(
    'expense_share',
    metadate,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('purchase_id', UUID(as_uuid=True), ForeignKey('purchase.id'), nullable=False),
    Column('user_id', UUID(as_uuid=True), ForeignKey('user.id'), nullable=False),
    Column('share_amount', Float, nullable=False),
)

comment = Table(
    'comment',
    metadate,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('meeting_id', UUID(as_uuid=True), ForeignKey('meeting.id'), nullable=False),
    Column('user_id', UUID(as_uuid=True), ForeignKey('user.id'), nullable=False),
    Column('content', String, nullable=False),
)

