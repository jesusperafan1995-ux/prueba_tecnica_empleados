from django.test import TestCase
from django.urls import reverse
from .models import Empleado
import json

class EmpleadoAPITest(TestCase):

    def setUp(self):

        self.empleado = Empleado.objects.create(
            nombre='Juan',
            apellido='Perez',
            documento='111111111',
            correo='juan@email.com',
            telefono='3001111111'
        )

        response = self.client.get('/api/empleados/')

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data['empleados']), 1)

    def test_listar_empleados(self):
    
            response = self.client.get(
                '/api/empleados/'
            )
    
            self.assertEqual(response.status_code, 200)

    def test_crear_empleado(self):

        cantidad_inicial = Empleado.objects.count()

        datos = {
            'nombre': 'Ana',
            'apellido': 'Gomez',
            'documento': '345678909',
            'correo': 'ana@email.com',
            'telefono': '3101234567'
        }

        response = self.client.post(
            '/api/empleados/crear/',
            data=datos,
            content_type='application/json'
        )

        print("RESPUESTA CREAR:", response.status_code, response.json())

        self.assertEqual(response.status_code, 201)

        self.assertEqual(Empleado.objects.count(), cantidad_inicial + 1)

    def test_crear_empleado_documento_duplicado(self):

        datos = {
            'nombre': 'Ana',
            'apellido': 'Gomez',
            'documento': '111111111',
            'correo': 'ana@email.com',
            'telefono': '3101234567'
        }

        response = self.client.post(
            '/api/empleados/crear/',
            data=json.dumps(datos),
            content_type='application/json'
        )

        print("RESPUESTA DOC. DUPLICADO:", response.status_code, response.json())

        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.json()['error'],
            'Ya existe un empleado con el mismo documento'
        )

    def test_crear_empleado_correo_duplicado(self):

        datos = {
            'nombre': 'Ana',
            'apellido': 'Gomez',
            'documento': '222222222',
            'correo': 'juan@email.com',
            'telefono': '3101234567'
        }

        response = self.client.post(
            '/api/empleados/crear/',
            data=json.dumps(datos),
            content_type='application/json'
        )

        print("RESPUESTA CORREO DUPLICADO:", response.status_code, response.json())

        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.json()['error'],
            'Ya existe un empleado con el mismo correo'
        )
    
    def test_crear_empleado_telefono_duplicado(self):

        datos = {
            'nombre': 'Ana',
            'apellido': 'Gomez',
            'documento': '222222222',
            'correo': 'ana@email.com',
            'telefono': '3001111111'
        }

        response = self.client.post(
            '/api/empleados/crear/',
            data=json.dumps(datos),
            content_type='application/json'
        )

        print("RESPUESTA TELÉFONO DUPLICADO:", response.status_code, response.json())

        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.json()['error'],
            'Ya existe un empleado con el mismo teléfono'
        )

    def test_detalle_empleado(self):

        response = self.client.get(
            f'/api/empleados/{self.empleado.id}/'
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data['nombre'], 'Juan')
        self.assertEqual(data['documento'], '111111111')

    def test_actualizar_empleado(self):

        response = self.client.get(
            f'/api/empleados/{self.empleado.id}/'
        )

        datos = {
            'nombre': 'Juan Carlos',
            'apellido': 'Perez',
            'documento': '111111111',
            'correo': 'juancarlos@email.com',
            'telefono': '3002222222'
        }

        response = self.client.put(
            f'/api/empleados/{self.empleado.id}/',
            data=datos,
            content_type='application/json'
        )

        print("STATUS:", response.status_code)
        print("RESPUESTA:", response.json())

        self.assertEqual(response.status_code, 200)

        self.empleado.refresh_from_db()

        self.assertEqual(self.empleado.nombre, 'Juan Carlos')
        self.assertEqual(self.empleado.correo, 'juancarlos@email.com')
        self.assertEqual(self.empleado.telefono, '3002222222')

    def test_eliminar_empleado(self):

        response = self.client.delete(
            f'/api/empleados/{self.empleado.id}/'
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Empleado.objects.filter(id=self.empleado.id).exists()
        )

    def test_empleado_no_existe(self):

        response = self.client.get(
            '/api/empleados/9999/'
        )

        self.assertEqual(response.status_code, 404)

        data = response.json()

        self.assertEqual(
            data['error'],
            'Empleado no encontrado'
        )

    def test_metodo_no_permitido(self):

        response = self.client.patch(
            f'/api/empleados/{self.empleado.id}/'
        )

        self.assertEqual(response.status_code, 405)

    def test_json_invalido(self):

        response = self.client.put(
            f'/api/empleados/{self.empleado.id}/',
            data='esto no es json',
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

        data = response.json()

        self.assertEqual(
            data['error'],
            'El formato JSON no es válido'
        )

    def test_crear_empleado_sin_nombre(self):

        data = {
            'nombre': '',
            'apellido': 'Perez',
            'documento': '222222222',
            'correo': 'test@test.com',
            'telefono': '3001234567'
        }

        response = self.client.post(
            '/api/empleados/crear/',
            data=json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)