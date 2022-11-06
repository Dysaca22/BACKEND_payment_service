from django.contrib import admin
from .models import Institution, Campus, Service, Program, Semester, Student, Bill, Pay

admin.site.register(Institution)
admin.site.register(Campus)
admin.site.register(Service)
admin.site.register(Program)
admin.site.register(Semester)
admin.site.register(Student)
admin.site.register(Bill)
admin.site.register(Pay)