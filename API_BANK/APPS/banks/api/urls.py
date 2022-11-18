from django.urls import path
from .api import bank_login, query_is_active


urlpatterns = [
    path('pay/login', bank_login, name='bank_login'),
    path('services/query', query_is_active, name='query_is_active'),
]