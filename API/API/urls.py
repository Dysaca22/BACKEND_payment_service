from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('APPS.users.api.urls')),
    path('institution/', include('APPS.institutions.api.urls')),
    path('service/', include('APPS.services.api.urls')),
]
