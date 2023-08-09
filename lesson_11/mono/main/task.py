import time
from celery import shared_task
from datetime import datetime
from .models import Card

@shared_task
def activate_card_async(card_id):
    time.sleep(120)
    card = Card.objects.get(pk=card_id)
    card.is_frozen = False
    card.save()

@shared_task
def freeze_expired_cards():
    today = datetime.now().date()
    expired_cards = Card.objects.filter(expiration_date__lt=today, is_frozen=False)

    for card in expired_cards:
        card.is_frozen = True
        card.save()