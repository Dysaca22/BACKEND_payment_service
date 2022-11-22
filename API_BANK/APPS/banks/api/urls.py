from django.urls import path
from .api import start_pay_or_consult, query_is_active, conn_with_passarella, make_transaction, transactions_list


urlpatterns = [
    path('conn_with_passarella', conn_with_passarella, name='conn_with_passarella'),
    path('service/query', query_is_active, name='query_is_active'),
    path('service/pay_consult', start_pay_or_consult, name='start_pay_or_consult'),
    path('service/transaction', make_transaction, name='make_transaction'),
    path('service/transaction_list', transactions_list, name='transactions_list'),
]