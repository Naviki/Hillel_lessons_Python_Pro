from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Card

class CardTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.client.force_authenticate(user=self.user)

    # Given
    def test_create_card(self):
        data = {
            'pan': '1111222233334444',
            'expiration_date': '08/2025',
            'cvv': '123',
            'issue_date': '2023-07-22',
            'card_name': 'My Card',
        }

        # When
        response = self.client.post('/cards/', data)

        # Then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(Card.objects.get().pan, '1111222233334444')
        self.assertEqual(Card.objects.get().owner, self.user)

    # Given
    def test_freeze_card(self):
        card = Card.objects.create(pan='1111222233334444', expiration_date='08/2025', cvv='123',
                                   issue_date='2023-07-22', owner=self.user)

        # When
        response = self.client.patch(f'/cards/{card.pk}/freeze/')

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Card.objects.get(pk=card.pk).is_frozen)

    # Given
    def test_unfreeze_card(self):
        card = Card.objects.create(pan='1111222233334444', expiration_date='08/2025', cvv='123',
                                   issue_date='2023-07-22', owner=self.user)
        card.is_frozen = True
        card.save()

        # When
        response = self.client.patch(f'/cards/{card.pk}/unfreeze/')

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Card.objects.get(pk=card.pk).is_frozen)

    # Given
    def test_view_own_cards(self):
        Card.objects.create(pan='1111222233334444', expiration_date='08/2025', cvv='123',
                            issue_date='2023-07-22', owner=self.user)
        Card.objects.create(pan='5555666677778888', expiration_date='12/2024', cvv='456',
                            issue_date='2023-07-22', owner=self.user)

        other_user = User.objects.create_user('otheruser', 'other@example.com', 'otherpassword')
        Card.objects.create(pan='9999000011112222', expiration_date='05/2026', cvv='789',
                            issue_date='2023-07-22', owner=other_user)

        # When
        response = self.client.get('/cards/')

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['pan'], '1111222233334444')
        self.assertEqual(response.data[1]['pan'], '5555666677778888')
