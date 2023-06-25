import uuid
from datetime import date
from creditcard import CreditCard
from code_db import create_table, save_to_database, get_from_database


create_table()


card = CreditCard(
    card_number='1234567890123456',
    expiration_date='12/24',
    cvv='123',
    issue_date=date.today(),
    owner_id=uuid.UUID('your_owner_id'),
    status='активна'
)


save_to_database(card)


retrieved_card = get_from_database('1234567890123456')

if retrieved_card:
    print('Отримано картку з бази даних.')
else:
    print('Картка не знайдена в базі даних.')
