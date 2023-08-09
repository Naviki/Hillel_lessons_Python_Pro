from django.contrib.auth.models import User
from django.db import models
from celery import shared_task


class CardManager(models.Manager):
    def is_valid(self, pan):
        digits = [int(x) for x in str(pan)]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        total = sum(odd_digits) + sum(sum(divmod(2 * x, 10)) for x in even_digits)
        return total % 10 == 0

class Card(models.Model):
    pan = models.CharField(max_length=16, unique=True)
    expiration_date = models.CharField(max_length=7)  # Format: MM/YYYY
    cvv = models.CharField(max_length=3)
    issue_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    card_name = models.CharField(max_length=255, blank=True, null=True)
    is_frozen = models.BooleanField(default=False)

    objects = CardManager()

    @shared_task
    def activate(self):
        from time import sleep
        sleep(120)  # Очікуємо 2 хвилини
        self.is_frozen = False
        self.save()
