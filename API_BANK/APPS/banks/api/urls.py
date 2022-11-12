from django.urls import path
from .api import bank_login


urlpatterns = [
    path('bank/pay/login', bank_login, name='bank_login'),
]