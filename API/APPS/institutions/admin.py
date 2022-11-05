from django.contrib import admin
from .models import Institution, Service, Student, StudentService

admin.site.register(Institution)
admin.site.register(Service)
admin.site.register(Student)
admin.site.register(StudentService)