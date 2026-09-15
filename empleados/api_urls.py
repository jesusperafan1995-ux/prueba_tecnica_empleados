from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_empleados, name='api_listar_empleados'),
    path('crear/', views.crear_empleado, name='api_crear_empleado'),
    path('<int:id>/', views.detalle_empleado, name='api_detalle_empleado'),
]