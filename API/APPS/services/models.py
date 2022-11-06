from django.db import models
from APPS.banks.models import Transaction
from APPS.institutions.models import Pay


class Shop(models.Model):
    _finished = models.BooleanField('Is finished', default=False)
    transaction = models.ForeignKey(Transaction, verbose_name='Bank transaction', on_delete=models.CASCADE)
    pay = models.ForeignKey(Pay, verbose_name='Institution oay', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'

    REQUIRED_FIELDS = '__all__'

    def __str__(self):
        return f'{self.id} - finished {self._finished}'