from django.urls import path
from .api import fase1, fase2, delete_fase1, delete_fase2


urlpatterns = [
    path('fase1', fase1, name='fase1'),
    path('fase2', fase2, name='fase2'),
    path('fase1/delete/<int:pk>', delete_fase1, name='delete_fase1'),
    path('fase2/delete/<int:pk>', delete_fase2, name='delete_fase2'),
]