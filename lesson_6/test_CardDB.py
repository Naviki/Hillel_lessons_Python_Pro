import sqlite3
import os
import pytest
from datetime import date
import uuid
from Card import CreditCard
from СardDB import create_table, save_to_database, get_from_database

TEST_DATABASE = 'test_cards.db'

@pytest.fixture(scope="module")
def setup_database():
    create_table()
    yield
    os.remove(TEST_DATABASE)

def test_save_to_database(setup_database):
    card = CreditCard("1234567890123456", "12/25", "123", date.today(), uuid.uuid4(), "активна")

    # when
    save_to_database(card)

    # then
    conn = sqlite3.connect(TEST_DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cards WHERE card_number=?", ("1234567890123456",))
    result = cursor.fetchone()
    conn.close()

    assert result is not None

def test_get_from_database(setup_database):
    card = CreditCard("1234567890123456", "12/25", "123", date.today(), uuid.uuid4(), "активна")
    save_to_database(card)

    # when
    retrieved_card = get_from_database("1234567890123456")

    # then
    assert retrieved_card is not None
    assert retrieved_card.card_number == "1234567890123456"
    assert retrieved_card.expiration_date == "12/25"
    assert retrieved_card.cvv == "123"
    assert retrieved_card.issue_date == date.today()
    assert retrieved_card.owner_id is not None
    assert retrieved_card.status == "активна"