from django.urls import path
from .api import login_api, register_api, get_user_data
from knox import views as knox_views
urlpatterns = [
    path('login/', login_api, name='login'),
    path('user/', get_user_data, name='get_user_data'),
    path('register/', register_api, name='register'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
]