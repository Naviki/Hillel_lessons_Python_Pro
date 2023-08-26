import datetime
import pytest
from lesson_16.models import Book, engine, Session

@pytest.fixture
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

def test_create_and_retrieve_book(session):
    # Given
    book_data = {
        'name': 'Sample Book',
        'author': 'John Doe',
        'date_of_release': datetime.date(2023, 1, 1),
        'description': 'A sample book for testing',
        'genre': 'Fiction'
    }

    # When
    book = Book(**book_data)
    session.add(book)
    session.commit()

    # Then
    retrieved_book = session.query(Book).filter_by(name='Sample Book').first()
    assert retrieved_book is not None
    assert retrieved_book.author == 'John Doe'
    assert retrieved_book.genre == 'Fiction'
