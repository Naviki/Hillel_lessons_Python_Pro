from django.test import TestCase
from rest_framework.test import APIClient
from .models.Card import CardModel


class CardModelTest(TestCase):
    def test_is_valid(self):
        # Given
        card = CardModel(
            PAN='4111111111111111',
            expiration_date='01/25',
            CVV='123',
            issue_date='2023-01-01',
            owner_id='0e6b22f7-90c2-4a6e-9c92-dc5a1e3a2e95'
        )

        # When
        result = card.is_valid()

        # Then
        self.assertTrue(result)

    def test_is_invalid(self):
        # Given
        card = CardModel(
            PAN='4111111111111112',
            expiration_date='01/25',
            CVV='123',
            issue_date='2023-01-01',
            owner_id='0e6b22f7-90c2-4a6e-9c92-dc5a1e3a2e95'
        )

        # When
        result = card.is_valid()

        # Then
        self.assertFalse(result)


class CardAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_card(self):
        # Given
        data = {
            'PAN': '4111111111111111',
            'expiration_date': '01/25',
            'CVV': '123',
            'issue_date': '2023-01-01',
            'owner_id': '0e6b22f7-90c2-4a6e-9c92-dc5a1e3a2e95'
        }

        # When
        response = self.client.post('/cards/', data)

        # Then
        self.assertEqual(response.status_code, 201)
        self.assertIn('success', response.data.get('message', ''))

    def test_get_card(self):
        # Given
        card = CardModel.objects.create(
            PAN='4111111111111111',
            expiration_date='01/25',
            CVV='123',
            issue_date='2023-01-01',
            owner_id='0e6b22f7-90c2-4a6e-9c92-dc5a1e3a2e95'
        )

        # When
        response = self.client.get(f'/cards/{card.id}/')

        # Then
        self.assertEqual(response.status_code, 200)
        expected_body = f'<td>{card.PAN}</td>'
        self.assertEqual(response.content.decode(), expected_body)
