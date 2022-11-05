from django.db import models
from APPS.users.models import User


class Service(models.Model):
    name = models.CharField('Name', max_length=255)
    value = models.DecimalField('Value', max_digits=9, decimal_places=2)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    REQUIRED_FIELDS = '__all__'

    def __str__(self):
        return f'{self.name}'


class Institution(models.Model):

    CAMPUS_ENUM = (
        ('BAQ', 'Barranquilla'),
        ('CTG', 'Cartagena'),
        ('SMR', 'Santa Marta'),
        ('SIN', 'Sincelejo'),
        ('MON', 'Monteria')
    )

    name = models.CharField('Name', max_length=255)
    campus = models.CharField('Campus', max_length=3, choices=CAMPUS_ENUM, default='BAQ')
    services = models.ManyToManyField(Service, verbose_name='Services', related_name='Institution', blank=True)

    class Meta:
        verbose_name = 'Institution'
        verbose_name_plural = 'Institutions'

    REQUIRED_FIELDS = '__all__'

    def __str__(self):
        return f'{self.name} - {self.campus}'


class Student(models.Model):
    name = models.CharField('Name', max_length=255)
    lastName = models.CharField('Last name', max_length=255)
    institution = models.ForeignKey(Institution, verbose_name='Institution', on_delete=models.CASCADE)
    user = models.OneToOneField(User, verbose_name='User', related_name='Student', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    REQUIRED_FIELDS = ['name', 'lastName', 'institution']

    def __str__(self):
        return f'{self.name} {self.lastName}'


class StudentService(models.Model):

    PAID_OPTION = (
        (True, 'Paid'),
        (False, 'Unpaid'),
    )

    service = models.ForeignKey(Service, verbose_name='Service', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, verbose_name='Student', on_delete=models.CASCADE)
    _status = models.BooleanField('Status', choices=PAID_OPTION, default=False)

    class Meta:
        verbose_name = 'Student service'
        verbose_name_plural = 'Student services'

    REQUIRED_FIELDS = '__all__'

    def __str__(self):
        return f'{self.service.name} - is {dict(self.PAID_OPTION)[self._status]}'