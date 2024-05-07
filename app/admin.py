from django.contrib import admin
from .models import Balance, Wallet, Transaction, Connection

# Register your models here.
admin.site.register(Balance)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Connection)