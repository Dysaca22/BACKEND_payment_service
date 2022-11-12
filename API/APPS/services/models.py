from django.db import models
from APPS.institutions.models import Pay


class Fase1(models.Model):

    TYPE_ENUM = (
        ('DC', 'Debit'),
        ('CC', 'Credit'),
    )

    email = models.EmailField('Email', max_length=255)
    payType = models.CharField('Pay type', max_length=2, choices=TYPE_ENUM)
    # Foreign keys
    payID = models.IntegerField('Pay ID')

    class Meta:
        verbose_name = 'Fase1'
        verbose_name_plural = 'Fases1'

    REQUIRED_FIELDS = '__all__'

    def __str__(self):
        return f'{self.id}'


class Fase2(models.Model):

    BANK_ENUM = (
        ('EB', 'East Bank'),
        ('WB', 'Western Bank'),
    )

    bank = models.CharField('Bank', max_length=2, choices=BANK_ENUM)
    name = models.CharField('Person name', max_length=255)
    lastName = models.CharField('Person last name', max_length=255)
    idNumber = models.CharField('Identification number', max_length=10)
    phone = models.CharField('Phone number', max_length=10)
    # Foreign keys
    fase1 = models.ForeignKey(Fase1, verbose_name='Fase1', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Fase2PSE'
        verbose_name_plural = 'Fases2PSE'

    REQUIRED_FIELDS = '__all__'

    def __str__(self):
        return f'{self.id}'


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