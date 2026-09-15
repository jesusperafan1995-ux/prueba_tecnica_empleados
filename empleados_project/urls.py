from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('empleados/', include('empleados.urls')),

    path('api/empleados/', include('empleados.api_urls')),
]