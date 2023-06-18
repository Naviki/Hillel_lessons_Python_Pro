from datetime import date
import uuid
from Card import CreditCard

def test_change_activation_status():
    card = CreditCard("1234567890123456", "12/25", "123", date.today(), uuid.uuid4(), "активна")

    # when
    card.change_activation_status("заблокована")

    # then
    assert card.status == "активна"

    # when
    card.change_activation_status("активна")

    # then
    assert card.status == "активна"

    # when
    card.block_card()
    card.change_activation_status("активна")

    # then
    assert card.status == "активна"

def test_block_card():
    card = CreditCard("1234567890123456", "12/25", "123", date.today(), uuid.uuid4(), "активна")

    # when
    card.block_card()

    # then
    assert card.status == "заблокована"

def test_mask_card_number():
    card = CreditCard("1234567890123456", "12/25", "123", date.today(), uuid.uuid4(), "активна")

    # when
    masked_card_number = card.mask_card_number()

    # then
    assert masked_card_number == "123456******3456"
