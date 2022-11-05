from django.urls import path
from .api import shop_detail_view, student_shop_api_view


urlpatterns = [
    path('shop/<int:pk>', shop_detail_view, name='shop_detail_api'),
    path('student/shop/<int:pk_student>', student_shop_api_view, name='student_shop_api'),
]