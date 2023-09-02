from sqlalchemy import create_engine, Column, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from MeetUpSplitter.config import DB_CONFIG

DATABASE_URL = f"postgresql://{DB_CONFIG['USER']}:{DB_CONFIG['PASSWORD']}@{DB_CONFIG['HOST']}:{DB_CONFIG['PORT']}/{DB_CONFIG['NAME']}"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'

    user_id = Column(String, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)

    meetings = relationship('Meeting', back_populates='creator')
    comments = relationship('Comment', back_populates='user')
    purchases = relationship('Purchase', back_populates='user')
    expense_shares = relationship('ExpenseShare', back_populates='user')

class Meeting(Base):
    __tablename__ = 'Meetings'

    meeting_id = Column(String, primary_key=True)
    place = Column(String)
    time = Column(DateTime)
    creator_id = Column(String, ForeignKey('Users.user_id'))

    creator = relationship('User', back_populates='meetings')
    participants = relationship('MeetingParticipant', back_populates='meeting')
    comments = relationship('Comment', back_populates='meeting')
    purchases = relationship('Purchase', back_populates='meeting')

class MeetingParticipant(Base):
    __tablename__ = 'Meeting_Participants'

    participant_id = Column(String, primary_key=True)
    meeting_id = Column(String, ForeignKey('Meetings.meeting_id'))
    user_id = Column(String, ForeignKey('Users.user_id'))

    meeting = relationship('Meeting', back_populates='participants')
    user = relationship('User', back_populates='meetings_attended')

class Purchase(Base):
    __tablename__ = 'Purchases'

    purchase_id = Column(String, primary_key=True)
    meeting_id = Column(String, ForeignKey('Meetings.meeting_id'))
    description = Column(String)
    amount = Column(DECIMAL)

    meeting = relationship('Meeting', back_populates='purchases')
    user = relationship('User', back_populates='purchases')
    expense_shares = relationship('ExpenseShare', back_populates='purchase')

class ExpenseShare(Base):
    __tablename__ = 'Expense_Shares'

    distribution_id = Column(String, primary_key=True)
    purchase_id = Column(String, ForeignKey('Purchases.purchase_id'))
    user_id = Column(String, ForeignKey('Users.user_id'))
    share_amount = Column(DECIMAL)

    user = relationship('User', back_populates='expense_shares')
    purchase = relationship('Purchase', back_populates='expense_shares')

class Comment(Base):
    __tablename__ = 'Comments'

    comment_id = Column(String, primary_key=True)
    meeting_id = Column(String, ForeignKey('Meetings.meeting_id'))
    user_id = Column(String, ForeignKey('Users.user_id'))
    content = Column(String)

    meeting = relationship('Meeting', back_populates='comments')
    user = relationship('User', back_populates='comments')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()