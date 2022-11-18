from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/institution/', include('APPS.institutions.api.urls')),
    path('api/user/', include('APPS.users.api.urls')),
    path('api/user/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/user/login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]