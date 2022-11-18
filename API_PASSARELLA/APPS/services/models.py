from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string


class ConnectionWithProvider(models.Model):

    STATUS_ENUM = (
        ('S', 'Successful'), 
        ('F', 'Failed'),
        ('C', 'Cancelled'),
        ('P', 'In process'),
    )

    id = models.TextField('Id', primary_key=True, blank=True)
    pay_id = models.IntegerField('Pay ID of institution')
    provider = models.CharField('Provider', max_length=100)
    concept = models.TextField('Concept')
    amount = models.DecimalField('Amount', max_digits=20, decimal_places=2)
    _status = models.CharField('Status', max_length=1, choices=STATUS_ENUM, default='P')
    _createdDate = models.DateTimeField('Creation date', default=timezone.now, editable=False)

    class Meta:
        verbose_name = 'Connection with provider'
        verbose_name_plural = 'Connections with providers'

    REQUIRED_FIELDS = ['pay_id', 'provider', 'concept', 'amount']

    def __str__(self):
        return f'{self.id}'

    def save(self, *args, **kwargs):
        self.id = f'{get_random_string(length=32)}'
        while ConnectionWithProvider.objects.filter(pk=self.id).first():
            self.id = f'{get_random_string(length=32)}'
        super(ConnectionWithProvider, self).save(*args, **kwargs)


class Phase1(models.Model):

    PAYMENT_METHOD = (
        ('DC', 'Debit card'),
        ('CC', 'Credit card'),
    )

    email = models.EmailField('Email',  max_length=254)
    payment_method = models.CharField('Payment method', max_length=2, choices=PAYMENT_METHOD)
    # Foreign keys
    connection_with_provider = models.ForeignKey(ConnectionWithProvider, verbose_name='Connection with provider', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Phase 1'
        verbose_name_plural = 'Phases 1'

    REQUIRED_FIELDS = '__all__'

    def __str__(self):
        return f'{self.id}'


class Phase2(models.Model):
    
    BANK_ENUM = (
        ('EB', 'East Bank'),
        ('WB', 'Western Bank'),
    )

    bank = models.CharField('Bank', max_length=2, choices=BANK_ENUM)
    name = models.CharField('Name', max_length=50)
    lastname = models.CharField('Last name', max_length=50)
    number_id = models.CharField('Number id', max_length=10)
    phone = models.CharField('Phone number', max_length=10)
    # Foreing keys
    phase1 = models.ForeignKey(Phase1, verbose_name='Phase 1', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Phase 2'
        verbose_name_plural = 'Phases 2'

    REQUIRED_FIELDS = '__all__'

    def __str__(self):
        return f'{self.id}'