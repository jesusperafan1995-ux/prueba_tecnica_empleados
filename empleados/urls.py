from django.urls import path
from . import views

urlpatterns = [
    #paginas
    path('', views.empleados_pagina, name='empleados'),
    path('crear/', views.crear_pagina, name='crear_empleado'),
    path('<int:id>/', views.detalle_pagina, name='detalle_empleado'),
]