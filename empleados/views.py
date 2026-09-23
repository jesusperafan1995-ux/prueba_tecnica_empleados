from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EmpleadoSerializer
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect   
from functools import wraps

import re
import json

from .models import Empleado

#login

def require_login(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('/empleados/login/')
        
        return view_func(request, *args, **kwargs)

    return wrapper

#paginas

@require_login
def empleados_pagina(request):

    return render(request, 'empleados/index.html')

@require_login
def detalle_pagina(request, id):

    return render(request, 'empleados/detalle.html', {
        'empleado_id': id
    })

@require_login
def crear_pagina(request):

    return render(request, 'empleados/crear.html')

#api

def listar_empleados(request):

    error = usuario_no_autenticado(request)

    if error:
        return error

    buscar = request.GET.get('buscar', '') 
    pagina = request.GET.get('pagina', 1)

    if buscar:
        empleados = Empleado.objects.filter(
            Q(nombre__icontains=buscar) |
            Q(apellido__icontains=buscar) |
            Q(documento__icontains=buscar) | 
            Q(correo__icontains=buscar) |
            Q(telefono__icontains=buscar)   
        )
    else:
        empleados = Empleado.objects.all()

    paginator = Paginator(empleados, 10) 
    pagina_actual = paginator.get_page(pagina)

    data = []

    for empleado in pagina_actual:
        data.append({
            'id': empleado.id,
            'nombre': empleado.nombre,
            'apellido': empleado.apellido,
            'documento': empleado.documento,
            'correo': empleado.correo,
            'telefono': empleado.telefono,
        })

    return JsonResponse({
            'empleados': data, 
            'pagina_actual': pagina_actual.number,
            'total_paginas': paginator.num_pages,
            'total_registros': paginator.count,
            'tiene_anterior': pagina_actual.has_previous(),
            'tiene_siguiente': pagina_actual.has_next(),
        })

@csrf_exempt
def detalle_empleado(request, id):

    error = usuario_no_autenticado(request)

    if error:
        return error

    try:
        empleado = Empleado.objects.get(id=id)

        if request.method == 'GET':

            data = {
                'id': empleado.id,
                'nombre': empleado.nombre,
                'apellido': empleado.apellido,
                'documento': empleado.documento,
                'correo': empleado.correo,
                'telefono': empleado.telefono,
            }

            return JsonResponse(data)

        elif request.method == 'PUT':

            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse(
                    {'error': 'El formato JSON no es válido'},
                    status=400
                )

            campos = ['nombre', 'apellido', 'documento', 'correo', 'telefono']

            error = validar_datos_empleado(data)
            
            if error:
                return JsonResponse({
                    'error': error
                }, status=400)

            try: 
                validate_email(data['correo'])
            except ValidationError:
                return JsonResponse({
                    'error': 'El correo electrónico no es válido'
                }, status=400)

            if Empleado.objects.filter(
                    documento=data['documento']
                ).exclude(
                    id=id
                ).exists():
                    return JsonResponse({
                        'error': 'Ya existe un empleado con el mismo documento'
                    }, status=400)
    
            if Empleado.objects.filter(correo=data['correo']).exclude(id=id).exists():
                return JsonResponse({
                    'error': 'Ya existe un empleado con el mismo correo'
                }, status=400)
    
            if Empleado.objects.filter(telefono=data['telefono']).exclude(id=id).exists():
                return JsonResponse({
                    'error': 'Ya existe un empleado con el mismo teléfono'
                }, status=400)

            for campo in campos:
                if campo not in data:
                    return JsonResponse(
                        {'error': f'El campo {campo} es obligatorio'},
                        status=400
                    )

            empleado.nombre = data['nombre']
            empleado.apellido = data['apellido']
            empleado.documento = data['documento']
            empleado.correo = data['correo']
            empleado.telefono = data['telefono']

            empleado.save()

            return JsonResponse({
                'mensaje': 'Empleado actualizado correctamente'
            })

        elif request.method == 'DELETE':

            empleado.delete()

            return JsonResponse({
                'mensaje': 'Empleado eliminado correctamente'
            })

        else:

            return JsonResponse(
                {'error': 'Método no permitido'},
                status=405
            )

    except Empleado.DoesNotExist:

        return JsonResponse(
            {'error': 'Empleado no encontrado'},
            status=404
        )
    
@csrf_exempt
def crear_empleado(request):

    error = usuario_no_autenticado(request)
    
    if error:
        return error

    if request.method != 'POST':
        return JsonResponse(
            {'error': 'Método no permitido'},
            status=405
        )

    try:
        data = json.loads(request.body)
        error = validar_datos_empleado(data)

        if error:
            return JsonResponse({
                'error': error
            }, status=400)

        try: 
            validate_email(data['correo'])
        except ValidationError:
            return JsonResponse({
                'error': 'El correo electrónico no es válido'
            }, status=400)

        if Empleado.objects.filter(documento=data['documento']
            ).exists():
            return JsonResponse({
                'error': 'Ya existe un empleado con el mismo documento'
            }, status=400)

        if Empleado.objects.filter(correo=data['correo']).exists():
            return JsonResponse({
                'error': 'Ya existe un empleado con el mismo correo'
            }, status=400)

        if Empleado.objects.filter(telefono=data['telefono']).exists():
            return JsonResponse({
                'error': 'Ya existe un empleado con el mismo teléfono'
            }, status=400)

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

def validar_datos_empleado(data, empleado_id = None):
    campos = ['nombre', 'apellido', 'documento', 'correo', 'telefono']

    for campo in campos:
        if campo not in data or not str(data[campo]).strip():
            return False, f'El campo {campo} es obligatorio'

    telefono = str(data['telefono']).strip()

    if not re.fullmatch(r'\d{10}', telefono):
        return False, 'El teléfono debe contener exactamente 10 dígitos'

    return None

@csrf_exempt
def login_empleado(request):

    if request.method != 'POST':
        return JsonResponse(    
            {'error': 'Metodo no permitido'},
            status=405
        )    

    try:
        data = json.loads(request.body)
        
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse(
                {'error': 'El usuario y contraseña obligatorios'},
                status=400
            ),
        
        usuario = authenticate (
            username=username, 
            password=password
        )

        if usuario is None:
            return JsonResponse({
                'error': 'Usuario o contraseña incorrectos'
            }, status=401)

        login(request, usuario)

        return JsonResponse({
            'mensaje': 'Inicio de sesión exitoso',
            'usuario': usuario.username
        })

    except json.JSONDecodeError:
        
        return JsonResponse({
            'error': 'El formato JSON no es válido'
            },status=400)

def usuario_no_autenticado(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'error': 'Debe iniciar sesion para acceder a este recurso'
        }, status=401)

    return None

@csrf_exempt
def logout_empleado(request):
    if request.method != 'POST':
        return JsonResponse(
            {'error': 'Método no permitido'},
            status=405
        )

    logout(request)

    return JsonResponse({
        'mensaje': 'Cierre de sesión exitoso'
    })

#serializador para la api rest framework

@api_view(['GET', 'POST'])
def empleados_drf(request):

    if request.method == 'GET':
        empleados = Empleado.objects.all()

        serializer = EmpleadoSerializer(empleados, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmpleadoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

@api_view(['GET'])
def obtener_csrf(request):
    token = get_token(request)
    return Response({'csrfToken': token})

@api_view(['GET', 'PUT', 'DELETE'])
def empleado_drf(request, id):
    try:
        empleado = Empleado.objects.get(id=id)
    except Empleado.DoesNotExist:
        return Response({'error': 'Empleado no encontrado'}, status=404)

    if request.method == 'GET':
        serializer = EmpleadoSerializer(empleado)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmpleadoSerializer(empleado, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        empleado.delete()
        return Response({'mensaje': 'Empleado eliminado correctamente'}, status=204)

def login_pagina(request):
    return render(request, 'empleados/login.html')