from django.db import models
from simple_history.models import HistoricalRecords
from dateutil.relativedelta import relativedelta
import datetime, random
from APPS.users.models import User


class Institution(models.Model):
    name = models.CharField('Name', max_length=255)

    class Meta:
        verbose_name = 'Institution'
        verbose_name_plural = 'Institutions'

    REQUIRED_FIELDS = '__all__'

    def __str__(self):
        return f'{self.name}'


class Campus(models.Model):

    CAMPUS_ENUM = (
        ('BAQ', 'Barranquilla'),
        ('CTG', 'Cartagena'),
        ('SMR', 'Santa Marta'),
        ('SIN', 'Sincelejo'),
        ('MON', 'Monteria'),
    )

    name = models.CharField('Name', max_length=255)
    city = models.CharField('City', max_length=3, choices=CAMPUS_ENUM, default='BAQ')
    # Foreign keys
    institution = models.ForeignKey(Institution, verbose_name='Institution', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Campus'
        verbose_name_plural = 'Campus'

    REQUIRED_FIELDS = '__all__'

    def __str__(self):
        return f'{self.institution.name} - {dict(self.CAMPUS_ENUM)[self.city]}'


class Service(models.Model):

    TYPE_ENUM = (
        ('PR', 'Pregrado'),
        ('PS', 'Posgrado'),
    )

    name = models.CharField('Name', max_length=255)
    type = models.CharField('Type', max_length=2, choices=TYPE_ENUM)
    # Foreign keys
    campus = models.ForeignKey(Campus, verbose_name='Campus', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    REQUIRED_FIELDS = '__all__'

    def __str__(self):
        return f'{self.name} - {self.campus}'

    @property
    def getType(self):
        return dict(self.TYPE_ENUM)[self.type]


class Program(models.Model):
    name = models.CharField('Name', max_length=255)
    # Foreign keys
    service = models.ForeignKey(Service, verbose_name='Service', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Program'
        verbose_name_plural = 'Programs'

    REQUIRED_FIELDS = '__all__'

    def __str__(self):
        return f'{self.name}'


class Semester(models.Model):
    
    YEAR_ENUM = (
        (r,r) for r in range(1984, datetime.date.today().year+1)
    )

    PERIOD_ENUM = (
        ('10', '10'),
        ('20', '20'),
        ('30', '30'),
    )

    year = models.IntegerField('Year', choices=YEAR_ENUM, default=datetime.datetime.now().year)
    period = models.CharField('Period', max_length=2, choices=PERIOD_ENUM)
    value = models.DecimalField('Value', max_digits=9, decimal_places=2)
    # Foreign keys
    program = models.ForeignKey(Program, verbose_name='Program', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Semester'
        verbose_name_plural = 'Semesters'

    REQUIRED_FIELDS = ['period', 'value', 'program']

    def __str__(self):
        return f'{self.year}_{self.period} - {self.program}'
    

class Student(models.Model):
    code = models.CharField('Code', max_length=10, unique=True, blank=True, editable=False)
    name = models.CharField('Name', max_length=255)
    lastName = models.CharField('Last name', max_length=255)
    # Foreign keys
    campus = models.ForeignKey(Campus, verbose_name='Campus', on_delete=models.CASCADE)
    user = models.OneToOneField(User, verbose_name='User', related_name='Student', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    REQUIRED_FIELDS = ['name', 'lastName', 'campus', 'user']

    def __str__(self):
        return f'{self.name} {self.lastName}'

    def save(self, *args, **kwargs):
        code = random.randint(1000000000, 9999999999)
        while Student.objects.filter(code=f'{code}'):
            code = random.randint(1000000000, 9999999999)
        self.code = f'{code}'
        super(Student, self).save(*args, **kwargs)


class Bill(models.Model):

    PAID_OPTION = (
        (True, 'Paid'),
        (False, 'Unpaid'),
    )

    _expiration = models.DateTimeField('Expiration date', editable=False)
    _generatedDate = models.DateTimeField('Creation date', default=datetime.datetime.now(), editable=False)
    _paid = models.BooleanField('Status', choices=PAID_OPTION, default=False)
    # Foreign keys
    semester = models.ForeignKey(Semester, verbose_name='Semester', null=True, on_delete=models.SET_NULL)
    student = models.ForeignKey(Student, verbose_name='Student', null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Bill'
        verbose_name_plural = 'Bills'

    REQUIRED_FIELDS = ['semester', 'student']

    def __str__(self):
        return f'{self.id}'

    @property
    def getPaid(self):
        return dict(self.PAID_OPTION)[self._paid]

    def save(self, *args, **kwargs):
        self._expiration = self._generatedDate + relativedelta(months=+1)
        super(Bill, self).save(*args, **kwargs)    


class Pay(models.Model):

    STATUS_ENUM = (
        ('S', 'Started'), 
        ('F', 'Finished'),
        ('P', 'In process'),
        ('C', 'cancelled'),
    )

    _date = models.DateTimeField('Creation date', default=datetime.datetime.now(), editable=False)
    _status = models.CharField('Status', max_length = 1, choices=STATUS_ENUM, default='P')
    # Foreign keys
    bills = models.ManyToManyField(Bill, related_name="Pay")
    student = models.ForeignKey(Student, verbose_name='Student', null=True, on_delete=models.SET_NULL)

    historical = HistoricalRecords()

    class Meta:
        verbose_name = 'Pay'
        verbose_name_plural = 'Pays'

    REQUIRED_FIELDS = ['bills', 'student']

    def __str__(self):
        return f'{self.id}'
    
    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value