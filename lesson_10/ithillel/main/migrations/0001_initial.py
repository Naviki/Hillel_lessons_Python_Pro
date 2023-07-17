# Generated by Django 4.2.3 on 2023-07-15 21:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CardModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PAN', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator('^\\d{16}$', 'Invalid PAN.')])),
                ('expiration_date', models.CharField(max_length=7)),
                ('CVV', models.CharField(max_length=3)),
                ('issue_date', models.DateField()),
                ('owner_id', models.UUIDField()),
            ],
            options={
                'db_table': 'main_card',
            },
        ),
    ]