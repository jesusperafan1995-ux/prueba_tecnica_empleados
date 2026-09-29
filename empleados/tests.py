from django.test import TestCase
from django.urls import reverse
from .models import Empleado
from django.contrib.auth.models import User
import json

class EmpleadoAPITest(TestCase):

    def setUp(self):

        self.usuario = User.objects.create_user(
            username='testuser',
            password='123456'
        )

        self.client.login(
            username='testuser',
            password='123456'
        )

        self.empleado = Empleado.objects.create(
            nombre='Juan',
            apellido='Perez',
            documento='111111111',
            correo='juan@email.com',
            telefono='3001111111'
        )
    # --- Listar con varios empleados (verifica contenido, no solo status) ---
    def test_listar_empleados_multiples(self):
        Empleado.objects.create(
            nombre='Ana',
            apellido='Gomez',
            documento='222222222',
            correo='ana@email.com',
            telefono='3002222222'
        )
        Empleado.objects.create(
            nombre='Luis',
            apellido='Diaz',
            documento='333333333',
            correo='luis@email.com',
            telefono='3003333333'
        )

        response = self.client.get('/api/empleados/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Ya había 1 en setUp, + 2 nuevos = 3
        self.assertEqual(len(data['empleados']), 3)

        documentos = [e['documento'] for e in data['empleados']]
        self.assertIn('111111111', documentos)
        self.assertIn('222222222', documentos)
        self.assertIn('333333333', documentos)


    def test_listar_empleados_inicial(self):
        response = self.client.get('/api/empleados/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['empleados']), 1)

    def test_listar_empleados(self):
        response = self.client.get('/api/empleados/')
        self.assertEqual(response.status_code, 200)

    def test_login_correcto(self):

        self.client.logout()

        datos = {
            'username': 'testuser',
            'password': '123456'
        }

        response = self.client.post(
            '/api/empleados/login/',
            data=json.dumps(datos),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.json()['mensaje'],
            'Inicio de sesión exitoso'
        )

    def test_login_credenciales_incorrectas(self):

        self.client.logout()

        datos = {
            'username': 'testuser',
            'password': 'incorrecta'
        }

        response = self.client.post(
            '/api/empleados/login/',
            data=json.dumps(datos),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 401)

    def test_login_json_invalido(self):

        self.client.logout()

        response = self.client.post(
            '/api/empleados/login/',
            data='esto no es json',
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    def test_login_metodo_no_permitido(self):

        self.client.logout()

        response = self.client.get(
            '/api/empleados/login/'
        )

        self.assertEqual(response.status_code, 405)

    def test_logout(self):

        response = self.client.post(
            '/api/empleados/logout/'
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            '_auth_user_id' in self.client.session
        )

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

        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.json()['error'],
            'Ya existe un empleado con el mismo correo'
        )

     # --- Correo con formato inválido ---
    def test_crear_empleado_correo_formato_invalido(self):
        datos = {
            'nombre': 'Carlos',
            'apellido': 'Ruiz',
            'documento': '444444444',
            'correo': 'esto-no-es-un-correo',
            'telefono': '3004444444'
        }

        response = self.client.post(
            '/api/empleados/crear/',
            data=json.dumps(datos),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
    
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

        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response.json()['error'],
            'Ya existe un empleado con el mismo teléfono'
        )

    def test_crear_empleado_telefono_formato_invalido(self):
        datos = {
            'nombre': 'Carlos',
            'apellido': 'Ruiz',
            'documento': '555555555',
            'correo': 'carlos@email.com',
            'telefono': 'abc123'  # no numérico
        }

        response = self.client.post(
            '/api/empleados/crear/',
            data=json.dumps(datos),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

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

        self.assertEqual(response.status_code, 200)
        self.empleado.refresh_from_db()

        self.assertEqual(self.empleado.nombre, 'Juan Carlos')
        self.assertEqual(self.empleado.correo, 'juancarlos@email.com')
        self.assertEqual(self.empleado.telefono, '3002222222')

    # --- Actualizar con documento duplicado de OTRO empleado ---
    def test_actualizar_empleado_documento_duplicado_de_otro(self):
        otro = Empleado.objects.create(
            nombre='Pedro',
            apellido='Lopez',
            documento='666666666',
            correo='pedro@email.com',
            telefono='3006666666'
        )

        datos = {
            'nombre': 'Pedro Editado',
            'apellido': 'Lopez',
            'documento': '111111111',
            'correo': 'pedro@email.com',
            'telefono': '3006666666'
        }

        response = self.client.put(
            f'/api/empleados/{otro.id}/',
            data=json.dumps(datos),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    def test_eliminar_empleado(self):

        response = self.client.delete(
            f'/api/empleados/{self.empleado.id}/'
        )

        self.assertEqual(response.status_code, 200)

        self.assertFalse(
            Empleado.objects.filter(id=self.empleado.id).exists()
        )

    # --- Eliminar un empleado que no existe ---
    def test_eliminar_empleado_no_existe(self):
        
        response = self.client.delete('/api/empleados/9999/')

        self.assertEqual(response.status_code, 404)


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

    def test_str_empleado(self):
        self.assertEqual(str(self.empleado), 'Juan Perez')

    