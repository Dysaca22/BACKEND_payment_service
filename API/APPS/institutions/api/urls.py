from django.urls import path
from .api import general_info_institution, create_student, general_info_student


urlpatterns = [
    path('', general_info_institution, name='general_info_institution'),
    path('create/', create_student, name='create_student'),
    path('student/<int:pk>', general_info_student, name='general_info_student'),
]