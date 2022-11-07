from django.urls import path
from .api import general_info_institution, user_student, general_info_student, student_by_code, missing_bills, generate_pay


urlpatterns = [
    path('', general_info_institution, name='general_info_institution'),
    path('user/<int:pk_user>', user_student, name='user_student'),
    path('student/<int:pk>', general_info_student, name='general_info_student'),
    path('student/pay/<int:code>', student_by_code, name='student_by_code'),
    path('student/pay/bills/<int:code>', missing_bills, name='missing_bills'),
    path('student/pay/bills/', generate_pay, name='generate_pay'),
]