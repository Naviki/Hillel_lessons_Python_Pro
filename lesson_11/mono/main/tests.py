from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Card
from datetime import timedelta
from django.utils import timezone

class CardTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.client.force_authenticate(user=self.user)

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

        # Verify data in the database
        card = Card.objects.get()
        self.assertEqual(card.pan, '1111222233334444')
        self.assertEqual(card.expiration_date, '08/2025')
        self.assertEqual(card.cvv, '123')
        self.assertEqual(str(card.issue_date), '2023-07-22')
        self.assertEqual(card.card_name, 'My Card')
        self.assertEqual(card.owner, self.user)

        # Verify response data
        self.assertEqual(response.data['pan'], '1111222233334444')
        self.assertEqual(response.data['expiration_date'], '08/2025')
        self.assertEqual(response.data['cvv'], '123')
        self.assertEqual(response.data['issue_date'], '2023-07-22')
        self.assertEqual(response.data['card_name'], 'My Card')
        self.assertEqual(response.data['owner'], self.user.id)

    def test_freeze_card(self):
        card = Card.objects.create(pan='1111222233334444', expiration_date='08/2025', cvv='123',
                                   issue_date='2023-07-22', owner=self.user)

        # When
        response = self.client.patch(f'/cards/{card.pk}/freeze/')

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Card.objects.get(pk=card.pk).is_frozen)
        self.assertEqual(response.data['is_frozen'], True)

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
        self.assertEqual(response.data['is_frozen'], False)

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
        self.assertEqual(response.data[0]['expiration_date'], '08/2025')
        self.assertEqual(response.data[0]['cvv'], '123')
        self.assertEqual(response.data[0]['issue_date'], '2023-07-22')
        self.assertEqual(response.data[0]['card_name'], '')
        self.assertEqual(response.data[0]['is_frozen'], False)
        self.assertEqual(response.data[0]['owner'], self.user.id)
        self.assertEqual(response.data[1]['pan'], '5555666677778888')

    def test_activate_card(self):
        card = Card.objects.create(pan='1111222233334444', expiration_date='08/2025', cvv='123',
                                   issue_date='2023-07-22', owner=self.user)

        # When
        response = self.client.patch(f'/cards/{card.pk}/activate/')

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Card.objects.get(pk=card.pk).is_active)
        self.assertEqual(response.data['is_active'], True)

    def test_auto_freeze_expired_cards(self):
        # Create a card that will expire in the past (yesterday)
        past_expiration = timezone.now() - timedelta(days=1)
        expired_card = Card.objects.create(pan='1234567890123456', expiration_date=past_expiration.strftime('%m/%Y'),
                                           cvv='789',
                                           issue_date='2023-07-22', owner=self.user)

        # Create a card that will expire in the future (tomorrow)
        future_expiration = timezone.now() + timedelta(days=1)
        future_card = Card.objects.create(pan='2345678901234567', expiration_date=future_expiration.strftime('%m/%Y'),
                                          cvv='123',
                                          issue_date='2023-07-22', owner=self.user)

        # When
        response = self.client.get('/cards/')  # Trigger the automatic freeze task

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Card.objects.get(pk=expired_card.pk).is_frozen)
        self.assertFalse(Card.objects.get(pk=future_card.pk).is_frozen)
