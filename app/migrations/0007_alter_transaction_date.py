# Generated by Django 5.0.4 on 2024-05-07 07:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_transaction_address_alter_transaction_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 7, 13, 13, 6, 961534), verbose_name='Date'),
        ),
    ]
