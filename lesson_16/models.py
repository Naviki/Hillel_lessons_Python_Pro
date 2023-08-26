import os
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    date_of_release = Column(Date, nullable=False)
    description = Column(String)
    genre = Column(String, nullable=False)


DB_CONFIG = {
    'NAME': os.environ.get('DB_NAME', 'card_base'),
    'USER': os.environ.get('DB_USER', 'Guest_user'),
    'PASSWORD': os.environ.get('DB_PASSWORD', '1488'),
    'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
    'PORT': os.environ.get('DB_PORT', '5432')
}

DB_URL = f"postgresql://{DB_CONFIG['USER']}:{DB_CONFIG['PASSWORD']}@{DB_CONFIG['HOST']}:{DB_CONFIG['PORT']}/{DB_CONFIG['NAME']}"

engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)
