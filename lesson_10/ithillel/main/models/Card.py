from django.db import models
from django.core.validators import RegexValidator


class Card(models.Model):
    PAN_validator = RegexValidator(r'^\d{16}$', 'Invalid PAN.')

    PAN = models.CharField(max_length=16, validators=[PAN_validator])
    expiration_date = models.CharField(max_length=7)  # 'місяць/рік' формат
    CVV = models.CharField(max_length=3)
    issue_date = models.DateField()
    owner_id = models.UUIDField()

    def is_valid(self):
        digits = [int(x) for x in str(self.PAN)]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        total = sum(odd_digits) + sum(sum(divmod(2 * x, 10)) for x in even_digits)
        return total % 10 == 0
