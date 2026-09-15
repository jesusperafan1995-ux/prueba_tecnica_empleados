from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Empleado

#paginas

def empleados_pagina(request):
    return render(request, 'empleados/index.html')


def detalle_pagina(request, id):
    return render(request, 'empleados/detalle.html', {
        'empleado_id': id
    })


def crear_pagina(request):
    return render(request, 'empleados/crear.html')

#api

def listar_empleados(request):
    empleados = Empleado.objects.all()

    data = []

    for empleado in empleados:
        data.append({
            'id': empleado.id,
            'nombre': empleado.nombre,
            'apellido': empleado.apellido,
            'documento': empleado.documento,
            'correo': empleado.correo,
            'telefono': empleado.telefono,
        })

    return JsonResponse(data, safe=False)


def detalle_empleado(request, id):
    try:
        empleado = Empleado.objects.get(id=id)

        data = {
            'id': empleado.id,
            'nombre': empleado.nombre,
            'apellido': empleado.apellido,
            'documento': empleado.documento,
            'correo': empleado.correo,
            'telefono': empleado.telefono,
        }

        return JsonResponse(data)

    except Empleado.DoesNotExist:
        return JsonResponse(
            {'error': 'Empleado no encontrado'},
            status=404
        )


@csrf_exempt
def crear_empleado(request):

    if request.method != 'POST':
        return JsonResponse(
            {'error': 'Método no permitido'},
            status=405
        )

    try:
        data = json.loads(request.body)

        empleado = Empleado.objects.create(
            nombre=data['nombre'],
            apellido=data['apellido'],
            documento=data['documento'],
            correo=data['correo'],
            telefono=data['telefono']
        )

        return JsonResponse({
            'mensaje': 'Empleado creado correctamente',
            'id': empleado.id
        }, status=201)

    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)