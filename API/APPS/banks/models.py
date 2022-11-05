from django.db import models
from django.utils import timezone
from random import randint


class Bank(models.Model):
    name = models.CharField('Name', max_length=255)

    class Meta:
        verbose_name = 'Bank'
        verbose_name_plural = 'Banks'

    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f'{self.name}'


class Service(models.Model):

    ACTIVE_OPTION = (
        (True, 'Active'),
        (False, 'Inactive'),
    )

    name = models.CharField('Name', max_length=50)
    bank = models.ForeignKey(Bank, verbose_name='Bank', on_delete=models.CASCADE)
    _status = models.BooleanField('Status', choices=ACTIVE_OPTION, default=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    REQUIRED_FIELDS = ['name', 'bank']

    def __str__(self):
        return f'{self.name} - is {dict(self.ACTIVE_OPTION)[self._status]}'


class Person(models.Model):
    name =  models.CharField('Name', max_length=50)
    lastName =  models.CharField('Last name', max_length=50)
    idNumber = models.CharField('Identification number', max_length=10, unique=True)
    email = models.EmailField('Email', max_length=255, unique=True)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'

    REQUIRED_FIELDS = ['name', 'lastName', 'idNumber', 'email']

    def __str__(self):
        return f'{self.name} {self.lastName}'


class Card(models.Model):

    TYPE_ENUM = (
        ('DC', 'Debit'),
        ('CC', 'Credit'),
    )

    ACTIVE_OPTION = (
        (True, 'Yes'),
        (False, 'No'),
    )

    bank = models.ForeignKey(Bank, verbose_name='Bank', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, verbose_name='Person', on_delete=models.CASCADE)
    type = models.CharField('Type', max_length=2, choices=TYPE_ENUM)
    number = models.CharField('Number', max_length=16, unique=True, editable=False)
    securityNumber = models.CharField('Security number', max_length=3, null=True, editable=False)
    balance = models.DecimalField('Balance', max_digits=10, decimal_places=2, default=0.0)
    _isActive = models.BooleanField('Is active', choices=ACTIVE_OPTION, default=True)
    _creationDate = models.DateField('Creation date', default=timezone.now, editable=False)

    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'

    REQUIRED_FIELDS = ['bank', 'person', 'type', 'balance']

    def __str__(self):
        return f'{dict(self.TYPE_ENUM)[self.type]} - {self.number}'

    def save(self, *args, **kwargs):
        number = randint(1000000000000000, 9999999999999999)
        while Card.objects.filter(number=number):
            number = randint(1000000000000000, 9999999999999999)
        self.number = f'{number:016d}'
        if self.type == 'CC':
            self.securityNumber = f'{randint(0, 999):03d}'
        self.balance = float(f'{self.balance:.2f}')
        super(Card, self).save(*args, **kwargs)


class Transaction(models.Model):

    STATUS_ENUM = (
        ('S', 'Successful'), 
        ('F', 'Failed'),
        ('P', 'In process'),
    )

    card = models.ForeignKey(Card, verbose_name='Card', null=True, editable=False, on_delete=models.SET_NULL)
    person = models.ForeignKey(Person, verbose_name='Payer', null=True, editable=False, on_delete=models.SET_NULL)
    amount = models.DecimalField('Amount', max_digits=9, decimal_places=2, editable=False,)
    concept = models.TextField('Concept', blank=True)
    _status = models.CharField('Status', max_length = 1, choices=STATUS_ENUM, default='P')
    _DateTime = models.DateTimeField('Date time', default=timezone.now, editable=False)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    REQUIRED_FIELDS = ['card', 'person', 'amount']

    def __str__(self):
        return f'{self.id}'

    def save(self, *args, **kwargs):
        self.amount = float(f'{self.amount:2f}')
        super(Transaction, self).save(*args, **kwargs)