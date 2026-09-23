from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('empleados')), 
    path('admin/', admin.site.urls),
    path('empleados/', include('empleados.urls')),
    path('api/empleados/', include('empleados.api_urls')),
    

]