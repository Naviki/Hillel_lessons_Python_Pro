from django.test import TestCase
from rest_framework.test import APIClient
from .models import Card

class CardModelTest(TestCase):
    def test_is_valid(self):
        # Створюємо Card
        card = Card(PAN='4111111111111111', expiration_date='01/25', CVV='123', issue_date='2023-01-01', owner_id='0e6b22f7-90c2-4a6e-9c92-dc5a1e3a2e95')
        self.assertTrue(card.is_valid())

    def test_is_invalid(self):
        # Створюємо Card з невалідним номером
        card = Card(PAN='4111111111111112', expiration_date='01/25', CVV='123', issue_date='2023-01-01', owner_id='0e6b22f7-90c2-4a6e-9c92-dc5a1e3a2e95')
        self.assertFalse(card.is_valid())

class CardAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_card(self):
        # Отримуємо відповідь від API при створенні картки
        response = self.client.post('/cards/', {'PAN': '4111111111111111', 'expiration_date': '01/25', 'CVV': '123', 'issue_date': '2023-01-01', 'owner_id': '0e6b22f7-90c2-4a6e-9c92-dc5a1e3a2e95'})
        self.assertEqual(response.status_code, 201)

    def test_get_card(self):
        # Створюємо тестовий об'єкт Card
        card = Card.objects.create(PAN='4111111111111111', expiration_date='01/25', CVV='123', issue_date='2023-01-01', owner_id='0e6b22f7-90c2-4a6e-9c92-dc5a1e3a2e95')

        # Отримуємо відповідь від API при отриманні картки
        response = self.client.get(f'/cards/{card.id}/')
        self.assertEqual(response.status_code, 200)