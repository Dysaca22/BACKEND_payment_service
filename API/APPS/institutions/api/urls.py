from django.urls import path
from .api import institution_information, institution_login, student_bills, student_bills_to_pay, delete_student_bills_to_pay, pay_information


urlpatterns = [
    path('', institution_information, name='institution_information'),
    path('student/login', institution_login, name='institution_login'),
    path('student/bills', student_bills, name='student_bills'),
    path('student/bills_to_pay', student_bills_to_pay, name='student_bills_to_pay'),
    path('student/bills_to_pay/<int:pk>', delete_student_bills_to_pay, name='delete_student_bills_to_pay'),
    path('student/pay/<int:pk>', pay_information, name='pay_information'),
]