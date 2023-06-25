import pytest
from datetime import date
from uuid import UUID
from creditcard import CreditCard
from code_db import save_to_database, get_from_database


@pytest.fixture
def sample_credit_card():
    return CreditCard(
        card_number="1234567890123456",
        expiration_date="12/25",
        cvv="123",
        issue_date=date.today(),
        owner_id=UUID("00000000-0000-0000-0000-000000000000"),
        status="active"
    )


@pytest.fixture
def sample_credit_card_number():
    return "1234567890123456"


def test_credit_card_creation(sample_credit_card):
    assert sample_credit_card.card_number == "1234567890123456"
    assert sample_credit_card.expiration_date == "12/25"
    assert sample_credit_card.cvv == "123"
    assert sample_credit_card.issue_date == date.today()
    assert sample_credit_card.owner_id == UUID("00000000-0000-0000-0000-000000000000")
    assert sample_credit_card.status == "active"


def test_change_activation_status(sample_credit_card):
    sample_credit_card.change_activation_status("inactive")
    assert sample_credit_card.status == "inactive"


def test_change_activation_status_blocked_card(sample_credit_card):
    sample_credit_card.status = "заблокована"
    sample_credit_card.change_activation_status("inactive")
    assert sample_credit_card.status == "заблокована"


def test_block_card(sample_credit_card):
    sample_credit_card.block_card()
    assert sample_credit_card.status == "заблокована"


def test_save_to_database(sample_credit_card):
    save_to_database(sample_credit_card)
    retrieved_card = get_from_database(sample_credit_card.card_number)
    assert retrieved_card.card_number == sample_credit_card.card_number
    assert retrieved_card.expiration_date == sample_credit_card.expiration_date
    assert retrieved_card.cvv == sample_credit_card.cvv
    assert retrieved_card.issue_date == sample_credit_card.issue_date
    assert retrieved_card.owner_id == sample_credit_card.owner_id
    assert retrieved_card.status == sample_credit_card.status


def test_get_from_database_nonexistent_card():
    retrieved_card = get_from_database("nonexistent_card_number")
    assert retrieved_card is None


def test_get_from_database(sample_credit_card, sample_credit_card_number):
    save_to_database(sample_credit_card)
    retrieved_card = get_from_database(sample_credit_card_number)
    assert retrieved_card.card_number == sample_credit_card.card_number
    assert retrieved_card.expiration_date == sample_credit_card.expiration_date
    assert retrieved_card.cvv == sample_credit_card.cvv
    assert retrieved_card.issue_date == sample_credit_card.issue_date
    assert retrieved_card.owner_id == sample_credit_card.owner_id
    assert retrieved_card.status == sample_credit_card.status
