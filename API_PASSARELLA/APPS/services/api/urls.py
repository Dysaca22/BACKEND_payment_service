from django.urls import path
from .api import conn_with_provider, start_passarella, phase1, phase2, finallize


urlpatterns = [
    path('conn_with_provider', conn_with_provider, name='conn_with_provider'),
    path('pay/<str:pk>', start_passarella, name='start_passarella'),
    path('phase1', phase1, name='phase1'),
    path('phase2', phase2, name='phase2'),
    path('finallize', finallize, name='finallize'),
]