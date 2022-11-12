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
    _finished = models.BooleanField('Is finished', default=False)
    # Extras
    value = models.DecimalField('Value', max_digits=9, decimal_places=2, blank=True)
    concept = models.CharField('Concept', max_length=500, blank=True)
    institution = models.CharField('Institution', max_length=100, blank=True)
    # Foreign keys
    fase1 = models.ForeignKey(Fase1, verbose_name='Fase1', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Fase2'
        verbose_name_plural = 'Fases2'

    REQUIRED_FIELDS = ['bank', 'name', 'lastName', 'idNumber', 'phone', 'fase1']

    def __str__(self):
        return f'{self.id}'

    def save(self, *args, **kwargs):
        pay = Pay.objects.filter(pk=self.fase1.payID).first()
        concept = 'Pago de'
        value = 0
        for bill in pay.bills.all():
            concept += f'{bill.semester.program.service.name.lower()} {bill.semester.program.name.lower()}'
            value += bill.semester.value
            if bill != [*pay.bills.all()][-1]:
                concept += ', '
            else: 
                concept += '.'
        self.value = value
        self.concept = concept
        self.institution = pay.student.campus.institution.name
        super(Fase2, self).save(*args, **kwargs)