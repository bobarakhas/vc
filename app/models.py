from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    btc = models.CharField(verbose_name='BTC (Cleared/Uncleared)', max_length=100, default='0.00000000/0.00000000', null=False, blank=False)
    xmr = models.CharField(verbose_name='XMR (Cleared/Uncleared)', max_length=100, default='0.00000000/0.00000000', null=False, blank=False)
    eth = models.CharField(verbose_name='ETH (Cleared/Uncleared)', max_length=100, default='0.00000000/0.00000000', null=False, blank=False)
    ltc = models.CharField(verbose_name='LTC (Cleared/Uncleared)', max_length=100, default='0.00000000/0.00000000', null=False, blank=False)

    def __str__(self):
        return self.user.username
    
class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    btc = models.CharField(verbose_name='BTC Wallet', max_length=100, default='')
    xmr = models.CharField(verbose_name='XMR Wallet', max_length=100, default='')
    eth = models.CharField(verbose_name='ETH Wallet', max_length=100, default='')
    ltc = models.CharField(verbose_name='LTC Wallet', max_length=100, default='')

    def __str__(self):
        return self.user.username

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    txnid = models.CharField(verbose_name='Txn ID', blank=False, null=False, max_length=100)
    txnhash = models.CharField(verbose_name='Txn Hash', blank=False, null=False, max_length=100)
    token = models.CharField(verbose_name='Token', blank=False, null=False, max_length=100)
    amount = models.CharField(verbose_name='Amount', blank=False, null=False, max_length=100)
    address = models.CharField(verbose_name='Address', blank=False, null=False, max_length=100)
    date = models.DateTimeField(verbose_name='Date', default=datetime.datetime.now(), blank=False, null=False)

    def __str__(self):
        return self.user.username
    
class Connection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    connections = models.TextField(verbose_name='Connections', default='', blank=True, null=True)

    def __str__(self):
        return self.user.username