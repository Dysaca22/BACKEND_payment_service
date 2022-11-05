from django.urls import path
from .api import person_detail_view
from .api import card_detail_view
from .api import person_card_api_view
from .api import transaction_api_view, transaction_detail_view
from .api import person_transaction_api_view


urlpatterns = [
    path('person/<int:pk>', person_detail_view, name='person_detail_api'),
    path('card/<int:pk>', card_detail_view, name='card_detail_api'),
    path('person/card/<int:pk_person>', person_card_api_view, name='person_card_detail_api'),
    path('transaction/', transaction_api_view, name='transaction_api'),
    path('transaction/<int:pk>', transaction_detail_view, name='transaction_detail_api'),
    path('person/transaction/<int:pk_person>', person_transaction_api_view, name='person_transaction_detail_api'),
]