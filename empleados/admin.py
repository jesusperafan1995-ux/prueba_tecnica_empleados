from django.contrib import admin
from .models import Empleado


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'documento', 'correo', 'telefono')
    search_fields = ('nombre', 'apellido', 'documento', 'correo')
