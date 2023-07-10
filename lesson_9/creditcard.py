import uuid
from datetime import date


class CreditCard:
    def __init__(self, card_number: str, expiration_date: str, cvv: str,
                 issue_date: date, owner_id: uuid.UUID, status: str):
        self.card_number = card_number
        self.expiration_date = expiration_date
        self.cvv = cvv
        self.issue_date = issue_date
        self.owner_id = owner_id
        self.status = status

    def change_activation_status(self, new_status: str):
        if self.status == 'заблокована':
            print("Картка заблокована і не може бути активована.")
        else:
            self.status = new_status
            self.save_to_database()

    def block_card(self):
        self.status = 'заблокована'
        self.save_to_database()

    def save_to_database(self):
        from lesson_8.code_db import save_to_database
        save_to_database(self)

    def mask_card_number(self):
        masked_card_number = self.card_number[:6] + '*' * (len(self.card_number) - 10) + self.card_number[-4:]
        return masked_card_number
