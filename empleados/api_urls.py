from django.urls import path
from . import views
from .views import (listar_empleados, crear_empleado, detalle_empleado, login_empleado, logout_empleado, empleados_drf)


urlpatterns = [
    path('', views.listar_empleados, name='api_listar_empleados'),
    path('crear/', views.crear_empleado, name='api_crear_empleado'),
    path('login/', views.login_empleado, name='api_login_empleado'),
    path('logout/', views.logout_empleado, name='api_logout_empleado'),

    path('drf/<int:id>/', views.empleado_drf, name='api_empleado_drf'),
    path('drf/', views.empleados_drf, name='api_empleados_drf'),

    path('<int:id>/', views.detalle_empleado, name='api_detalle_empleado'),

    path('csrf/', views.obtener_csrf, name='api_csrf'),
]