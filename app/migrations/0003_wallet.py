# Generated by Django 5.0.4 on 2024-05-05 20:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_balance_ltc_alter_balance_btc_alter_balance_eth_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('btc', models.CharField(default='', max_length=100, verbose_name='BTC Wallet')),
                ('xmr', models.CharField(default='', max_length=100, verbose_name='XMR Wallet')),
                ('eth', models.CharField(default='', max_length=100, verbose_name='ETH Wallet')),
                ('ltc', models.CharField(default='', max_length=100, verbose_name='LTC Wallet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
