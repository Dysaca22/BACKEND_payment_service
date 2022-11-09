from django.urls import path
from API.APPS.users import views
from knox import views as knox_views
urlpatterns = [
    path('login/', views.login_api, name='login'),
    path('user/', views.get_user_data, name='get_user_data'),
    path('register/', views.register_api, name='register'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
]