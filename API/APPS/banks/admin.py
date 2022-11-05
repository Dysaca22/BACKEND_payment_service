from django.contrib import admin
from .models import Bank, Service, Person, Card, Transaction

admin.site.register(Bank)
admin.site.register(Service)
admin.site.register(Person)
admin.site.register(Card)
admin.site.register(Transaction)