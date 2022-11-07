from django.db import models
from APPS.institutions.models import Pay


class Shop(models.Model):

    TYPE_ENUM = (
        ('DC', 'Debit'),
        ('CC', 'Credit'),
    )

    _finished = models.BooleanField('Is finished', default=False)
    # Transaction
    amount = models.DecimalField('Amount', max_digits=9, decimal_places=2, editable=False)
    concept = models.TextField('Concept', blank=True)
    # Card
    type = models.CharField('Type', max_length=2, choices=TYPE_ENUM)
    number = models.CharField('Number', max_length=16, unique=True, editable=False)
    # Bank
    name = models.CharField('Name', max_length=255)
    # Person 
    name =  models.CharField('Name', max_length=50)
    lastName =  models.CharField('Last name', max_length=50)
    # Foreign keys
    pay = models.ForeignKey(Pay, verbose_name='Institution pay', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'

    REQUIRED_FIELDS = '__all__'

    def __str__(self):
        return f'{self.id} - finished {self._finished}'