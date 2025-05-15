# Arquitectura del Backend biblioteca

## Servicios Principales

El backend de Biblioteca 210 implementa los siguientes servicios fundamentales:
- **Gestión de Inventario:** Alta, modificación, consulta y eliminación de libros, materiales, mapas, multimedia, notebooks y proyectores.
- **Gestión de Usuarios:** Registro, autenticación y permisos para usuarios y personal administrativo.
- **Gestión de Préstamos:** Registro y control de préstamos y devoluciones de materiales.
- **Reportes y Consultas:** Generación de reportes y consultas avanzadas sobre el inventario y movimientos.

## Flujo de Autenticación Mejorado

La autenticación se basa en el sistema SIMEF:
1. El usuario accede a la página de login y envía sus credenciales.
2. SIMEF verifica usuario y contraseña contra la base de datos.
3. Si la autenticación es exitosa, se crea una sesión segura para el usuario.
4. En el apartado Bliblioteca de SIMEF se ingresa al sistema.

## Estructura de Directorios del Backend

```
├── biblioteca_digital/
│   ├── __init__.py
│   ├── settings.py         # Configuración general del proyecto
│   ├── urls.py             # Rutas principales del backend
│   ├── wsgi.py             # Interfaz de servidor WSGI
│   ├── libros/             # Módulo principal de inventario
│   │   ├── models.py       # Modelos de datos para libros
│   │   ├── views.py        # Vistas backend de libros
│   │   ├── admin.py       # Configuración del admin de Django
│   │   ├── migrations/     # Migraciones de base de datos
│   │   └── tests.py        # Pruebas unitarias
│   ├── materiales/
│   │   ├── models.py
│   │   ├── views.py
│   │   └── migrations/
│   ├── usuarios/
│   │   ├── models.py       # Modelos de usuarios
│   │   ├── views.py        # Vistas de gestión de usuarios
│   │   └── migrations/
│   └── utils/              # Utilidades y helpers
├── db.sqlite3              # Base de datos SQLite
├── manage.py             # Script de gestión de Django
└── requirements.txt       # Dependencias del proyecto
```

### Descripción de Directorios
- **`biblioteca_digital/`**: Directorio raíz del proyecto Django
- **`libros/`**: Módulo para gestión de libros
- **`materiales/`**: Módulo para gestión de otros materiales
- **`usuarios/`**: Módulo para gestión de usuarios
- **`utils/`**: Funciones y clases de utilidad

### Archivos Clave
- **`settings.py`**: Configuraciones globales del proyecto
- **`urls.py`**: Definición de rutas URL
- **`manage.py`**: Herramienta de administración de Django
- **`requirements.txt`**: Lista de dependencias del proyecto

## Dependencias Clave

- **Django:** Framework principal para el desarrollo web y ORM.
- **Pillow:** Manejo de imágenes.
- **SQLite3:** Base de datos ligera y fácil de administrar.
- **Herramientas estándar de Python:** Para utilidades y scripts auxiliares.

**Instalación recomendada:**
```bash
pip install django pillow
```

**Nota:** Se recomienda mantener las dependencias actualizadas y documentadas en un archivo `requirements.txt`.

