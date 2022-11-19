from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from random import randint
from APPS.users.models import NewUser as User
from django.utils.crypto import get_random_string


class Bank(models.Model):

    BANK_ENUM = (
        ('EB', 'East Bank'),
        ('WB', 'Western Bank'),
    )

    name = models.CharField('Name', choices=BANK_ENUM, unique=True, max_length=2)

    class Meta:
        verbose_name = 'Bank'
        verbose_name_plural = 'Banks'

    REQUIRED_FIELDS = '__all__'

    def __str__(self):
        return f'{dict(self.BANK_ENUM)[self.name]}'


class Service(models.Model):

    TYPE_SERVICE = (
        ('C', 'Consult'),
        ('P', 'Pay'),
    )

    ACTIVE_OPTION = (
        (True, 'Active'),
        (False, 'Inactive'),
    )

    name = models.CharField('Name', max_length=1, choices=TYPE_SERVICE)
    _status = models.BooleanField('Status', choices=ACTIVE_OPTION, default=True)
    # Foreign keys
    bank = models.ForeignKey(Bank, verbose_name='Bank', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    REQUIRED_FIELDS = ['name', 'bank']

    def __str__(self):
        return f'{self.bank} {dict(self.TYPE_SERVICE)[self.name]} - is {dict(self.ACTIVE_OPTION)[self._status]}'


class Person(models.Model):
    name = models.CharField('Name', max_length=50)
    lastName = models.CharField('Last name', max_length=50)
    email = models.EmailField('Email', max_length=254)
    idNumber = models.CharField('Identification number', max_length=10, unique=True)
    # Foreign keys
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'

    REQUIRED_FIELDS = '__all__'

    def __str__(self):
        return f'{self.name} {self.lastName}'


class Card(models.Model):

    ACTIVE_OPTION = (
        (True, 'Yes'),
        (False, 'No'),
    )

    number = models.CharField('Number', max_length=16, primary_key=True, blank=True)
    _isActive = models.BooleanField('Is active', choices=ACTIVE_OPTION, default=True)
    _creationDate = models.DateField('Creation date', default=timezone.now, editable=False)
    # Foreign keys
    bank = models.ForeignKey(Bank, verbose_name='Bank', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, verbose_name='Person', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'

    REQUIRED_FIELDS = ['bank', 'person']

    def save(self, *args, **kwargs):
        if not self.number:
            number = randint(1000000000000000, 9999999999999999)
            while Card.objects.filter(number=number).first():
                number = randint(1000000000000000, 9999999999999999)
            self.number = f'{number:016d}'
        super(Card, self).save(*args, **kwargs)


class DebitCard(Card):
    balance = models.DecimalField('Balance', max_digits=20, decimal_places=2, default=0.0)

    def __str__(self):
        return f'DC {self.number}'

    class Meta:
        verbose_name = 'Debit card'
        verbose_name_plural = 'Debit cards'

    REQUIRED_FIELDS = ['bank', 'person', 'balance']


class CreditCard(Card):

    TYPE_ENUM = (
        ('VS', 'Visa'),
        ('MC', 'Mastercard'),
        ('AE', 'Ametican Express'),
    )

    securityNumber = models.CharField('Security number', max_length=3, null=True, editable=False)
    quota = models.DecimalField('Quota', max_digits=10, decimal_places=2, default=0.0)
    type = models.CharField('Type', max_length=2, choices=TYPE_ENUM, editable=False)

    def __str__(self):
        return f'CC {self.number}'

    class Meta:
        verbose_name = 'Credit card'
        verbose_name_plural = 'Credit cards'

    REQUIRED_FIELDS = ['bank', 'person', 'quota', 'type']

    def save(self, *args, **kwargs):
        if not self.securityNumber:
            self.securityNumber = f'{randint(100, 999):03d}'
        super(CreditCard, self).save(*args, **kwargs)


class ConnectionWithPassarella(models.Model):

    STATUS_ENUM = (
        ('S', 'Successful'), 
        ('F', 'Failed'),
        ('C', 'Cancelled'),
        ('P', 'In process'),
    )

    id = models.TextField('Id', primary_key=True, blank=True)
    passarella_id = models.TextField('Passarella ID of institution')
    provider = models.CharField('Provider', max_length=100)
    concept = models.TextField('Concept')
    amount = models.DecimalField('Amount', max_digits=20, decimal_places=2)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    _status = models.CharField('Status', max_length=1, choices=STATUS_ENUM, default='P')
    _createdDate = models.DateTimeField('Creation date', default=timezone.now, editable=False)

    class Meta:
        verbose_name = 'Connection with passarella'
        verbose_name_plural = 'Connections with passarellas'

    REQUIRED_FIELDS = ['passarella_id', 'provider', 'concept', 'amount']

    def __str__(self):
        return f'{self.id}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = f'{get_random_string(length=32)}'
            while ConnectionWithPassarella.objects.filter(pk=self.id).first():
                self.id = f'{get_random_string(length=32)}'
        super(ConnectionWithPassarella, self).save(*args, **kwargs)


class Transaction(models.Model):

    number_bill = models.CharField('Number bill', max_length=20, primary_key=True, blank=True)
    process_of_pay = models.ForeignKey(ConnectionWithPassarella, verbose_name='Information of pay', on_delete=models.CASCADE)
    _createdDate = models.DateTimeField('Creation date', default=timezone.now, editable=False)
    # Foreign keys
    card = models.ForeignKey(Card, verbose_name='Card', blank=True, null=True, on_delete=models.SET_NULL)

    historical = HistoricalRecords()

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    REQUIRED_FIELDS = ['process_of_pay', 'card']

    def __str__(self):
        return f'{self.id}'

    def save(self, *args, **kwargs):
        if not self.number_bill:
            number_bill = randint(10000000000000000000, 99999999999999999999)
            while Transaction.objects.filter(number_bill=number_bill).first():
                number_bill = randint(10000000000000000000, 99999999999999999999)
            self.number_bill = f'{number_bill:020d}'
        super(Transaction, self).save(*args, **kwargs)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value