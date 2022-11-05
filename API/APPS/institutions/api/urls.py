from django.urls import path
from .api import institution_api_view, institution_detail_view
from .api import student_api_view, student_detail_view
from .api import student_service_api_view, student_service_detail_view


urlpatterns = [
    path('institution/', institution_api_view, name='institution_api'),
    path('institution/<int:pk>', institution_detail_view, name='institution_detail_api'),
    path('studente/', student_api_view, name='student_api'),
    path('studente/<int:pk>', student_detail_view, name='student_detail_api'),
    path('student/service/<int:pk_student>', student_service_api_view, name='student_service_api'),
    path('student/service/<int:pk>', student_service_detail_view, name='student_service_detail_api'),
]