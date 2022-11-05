from django.db import models
from APPS.banks.models import Transaction
from APPS.institutions.models import StudentService


class Shop(models.Model):
    transaction = models.ForeignKey(Transaction, verbose_name='Transaction', on_delete=models.CASCADE)
    service = models.ForeignKey(StudentService, verbose_name='Institution service', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'

    REQUIRED_FIELDS = ['transaction', 'service']

    def __str__(self):
        return f'{self.name} - is {dict(self.ACTIVE_OPTION)[self._status]}'