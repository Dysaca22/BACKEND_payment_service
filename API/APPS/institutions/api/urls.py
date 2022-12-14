from django.urls import path
from .api import institution_information, student_profile, student_bills, student_bills_to_pay, delete_student_pay, pay_information, finallize


urlpatterns = [
    path('', institution_information, name='institution_information'),
    path('student/profile', student_profile, name='student_profile'),
    path('student/bills', student_bills, name='student_bills'),
    path('student/bills_to_pay', student_bills_to_pay, name='student_bills_to_pay'),
    path('student/pay/delete/<int:pk>', delete_student_pay, name='delete_student_pay'),
    path('student/pay/<int:pk>', pay_information, name='pay_information'),
    path('student/pay/finallize', finallize, name='finallize'),
]