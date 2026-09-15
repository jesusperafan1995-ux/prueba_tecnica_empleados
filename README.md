# Prueba Técnica - Gestión de Empleados

Aplicación web desarrollada como prueba técnica para la gestión básica de empleados, utilizando Django como framework backend, MySQL como base de datos y JavaScript para la interacción con la API REST.

## Tecnologías utilizadas

* Python 3.14
* Django 5.2
* MySQL 8.0
* JavaScript
* HTML5
* Bootstrap 5
* Git

## Funcionalidades

La aplicación permite:

* Listar empleados.
* Consultar el detalle de un empleado mediante una ruta dinámica.
* Crear nuevos empleados.
* Consultar información mediante una API REST.
* Intercambiar información entre frontend y backend utilizando JSON.
* Realizar consultas mediante JavaScript 'fetch()'.
* Utilizar solicitudes GET para consultar el detalle de un empleado.
* Utilizar solicitudes POST para crear empleados.
* Persistir la información en MySQL.
* Administrar empleados mediante el panel administrativo de Django.
* Configurar las credenciales de la base de datos mediante variables de entorno.

## Datos del empleado

Cada empleado contiene los siguientes campos:

* Nombre
* Apellido
* Número de documento
* Correo electrónico
* Teléfono

## Estructura de rutas

### Aplicación web

| Ruta                | Descripción                       |
| ------------------- | --------------------------------- |
| '/empleados/'       | Listado de empleados              |
| '/empleados/<id>/'  | Detalle de un empleado            |
| '/empleados/crear/' | Formulario para crear un empleado |

### API REST

| Ruta                    | Método | Descripción                        |
| ----------------------- | ------ | ---------------------------------- |
| '/api/empleados/'       | GET    | Lista todos los empleados          |
| '/api/empleados/<id>/'  | GET    | Consulta el detalle de un empleado |
| '/api/empleados/crear/' | POST   | Crea un nuevo empleado             |

### Administración

| Ruta      | Descripción                    |
| --------- | ------------------------------ |
| '/admin/' | Panel administrativo de Django |

## Instalación

### 1. Clonar el repositorio

'''bash
git clone URL_DEL_REPOSITORIO
cd prueba_tecnica
'''

### 2. Crear el entorno virtual

En Windows:

'''bash
python -m venv venv
'''

Activar el entorno virtual:

'''bash
venv\Scripts\activate
'''

### 3. Instalar las dependencias

'''bash
python -m pip install -r requirements.txt
'''

### 4. Configurar las variables de entorno

Crear un archivo '.env' en la raíz del proyecto tomando como referencia '.env.example'.

El archivo '.env' debe contener:

'''text
DB_NAME=empleados_db
DB_USER=root
DB_PASSWORD=TU_CONTRASEÑA
DB_HOST=localhost
DB_PORT=3306
'''

> El archivo '.env' contiene información sensible y no debe ser incluido en el repositorio.

### 5. Crear la base de datos

Ingresar a MySQL y ejecutar:

'''sql
CREATE DATABASE empleados_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
'''

### 6. Ejecutar las migraciones

Desde la carpeta raíz del proyecto:

'''bash
python manage.py migrate
'''

Esto creará las tablas necesarias para la aplicación.

### 7. Crear un usuario administrador

Para acceder al panel administrativo de Django:

'''bash
python manage.py createsuperuser
'''

Seguir las instrucciones mostradas en la consola.

### 8. Ejecutar el servidor

'''bash
python manage.py runserver
'''

La aplicación estará disponible en:

'''text
http://127.0.0.1:8000/
'''

El listado de empleados estará disponible en:

'''text
http://127.0.0.1:8000/empleados/
'''

El panel administrativo estará disponible en:

'''text
http://127.0.0.1:8000/admin/
'''

## API

La aplicación cuenta con endpoints REST que utilizan JSON para la comunicación entre frontend y backend.

### Listar empleados

'''http
GET /api/empleados/
'''

Ejemplo de respuesta:

'''json
[
    {
        "id": 1,
        "nombre": "Juan",
        "apellido": "Pérez",
        "documento": "123456789",
        "correo": "juan@example.com",
        "telefono": "3001234567"
    }
]
'''

### Consultar detalle

'''http
GET /api/empleados/1/
'''

Ejemplo de respuesta:

'''json
{
    "id": 1,
    "nombre": "Juan",
    "apellido": "Pérez",
    "documento": "123456789",
    "correo": "juan@example.com",
    "telefono": "3001234567"
}
'''

### Crear empleado

'''http
POST /api/empleados/crear/
'''

Ejemplo de solicitud:

'''json
{
    "nombre": "Carlos",
    "apellido": "Ramírez",
    "documento": "123456789",
    "correo": "carlos@example.com",
    "telefono": "3001234567"
}
'''

## Estructura del proyecto

'''text
prueba_tecnica/
│
├── empleados/
│   ├── migrations/
│   ├── templates/
│   │   └── empleados/
│   │       ├── index.html
│   │       ├── detalle.html
│   │       └── crear.html
│   ├── admin.py
│   ├── api_urls.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── empleados_project/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
'''

## Configuración de seguridad

Las credenciales de conexión a MySQL se gestionan mediante variables de entorno.

El archivo '.env' está excluido del control de versiones mediante '.gitignore', evitando publicar credenciales sensibles en el repositorio.

## Notas

Este proyecto fue desarrollado como una aplicación sencilla y funcional para demostrar conocimientos en desarrollo web con Django, integración con MySQL, creación y consumo de APIs REST, manejo de JSON y comunicación mediante JavaScript 'fetch()'.

La aplicación puede ser ampliada posteriormente con funcionalidades como edición y eliminación de empleados, autenticación de usuarios, validaciones adicionales, paginación y mejoras de seguridad.
