from django.db import models
from django.core.validators import RegexValidator


class CardManager(models.Manager):
    def is_valid(self, pan):
        digits = [int(x) for x in str(pan)]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        total = sum(odd_digits) + sum(sum(divmod(2 * x, 10)) for x in even_digits)
        return total % 10 == 0

class CardModel(models.Model):
    PAN_validator = RegexValidator(r'^\d{16}$', 'Invalid PAN.')

    PAN = models.CharField(max_length=16, validators=[PAN_validator])
    expiration_date = models.CharField(max_length=7)
    CVV = models.CharField(max_length=3)
    issue_date = models.DateField()
    owner_id = models.UUIDField()

    objects = CardManager()

    class Meta:
        db_table = 'main_card'