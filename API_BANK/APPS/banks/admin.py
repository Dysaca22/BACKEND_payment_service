from django.contrib import admin
from .models import Bank, Service, Person, Card, DebitCard, CreditCard, Transaction, ConnectionWithPassarella

admin.site.register(Bank)
admin.site.register(Service)
admin.site.register(Person)
admin.site.register(Card)
admin.site.register(DebitCard)
admin.site.register(CreditCard)
admin.site.register(Transaction)
admin.site.register(ConnectionWithPassarella)