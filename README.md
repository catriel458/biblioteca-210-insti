# Biblioteca 210 📚

Sistema de gestión de biblioteca del Instituto 210, construido en Django. Incluye autenticación, gestión de usuarios, administración de materiales (libros, mapas, multimedia, notebooks, proyectores, varios y programas), registro de bajas y préstamos.

## 🧰 Tecnologías

- Django 4.2.x
- Python 3.9+ (recomendado 3.10/3.11)
- SQLite por defecto (MySQL opcional)

## 🌟 Funcionalidades

- Autenticación: login, registro, perfil y cambio de contraseña.
- Roles: acceso de gestión para perfil `bibliotecaria`.
- Gestión de usuarios: buscar, crear, editar, eliminar (con validaciones y protección de último bibliotecario).
- Materiales: altas, bajas, edición y reactivación de `Libro`, `Mapas`, `Multimedia`, `Notebook`, `Proyector`, `Varios` y `Programa`.
- Préstamos: solicitar, aprobar/rechazar, finalizar, confirmar retiro, marcar no-retiro.
- Registro de bajas e informes para reactivación.
- Búsquedas rápidas (endpoints JSON) por título/autor, tipo, modelo, etc.
- Carga de materiales por CSV.

## 🚀 Instalación (Windows)

1. Clonar el repositorio
   `git clone https://github.com/catriel458/biblioteca-210-insti.git`
2. Crear y activar entorno virtual 
   - `python -m venv .venv`
   - `.venv\Scripts\activate`
3. Instalar dependencias
   `pip install -r requirements.txt`
4. Migraciones de base de datos
   `python manage.py migrate`
5. Crear superusuario (para admin/gestión)
   `python manage.py createsuperuser`
6. Ejecutar servidor de desarrollo
   `python manage.py runserver`
7. Acceder en el navegador
   `http://127.0.0.1:8000/`

## ⚙️ Configuración

- Static y Media:
  - `STATIC_URL = 'static/'` con archivos en `materiales/static`.
  - `MEDIA_URL = '/media/'`, `MEDIA_ROOT = media/`. Se crea automáticamente `media/imagenes_rota`.
- Base de datos por defecto: SQLite (`db.sqlite3`).
- MySQL opcional: en `biblioteca_digital/settings.py` hay un bloque comentado para MySQL. Variables esperadas:
  - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.
  - Descomenta el bloque y configura tus variables (puedes usar `.env`).

## 🧭 Rutas principales

- Autenticación y navegación:
  - `/` y `/login/` (inicio de sesión)
  - `/registro/`, `/logout/`, `/perfil/`, `/cambiar-password/`
  - `/home/` (inicio), `/gestion/` (panel de gestión)
- Gestión de usuarios:
  - `/gestion/usuarios/`, `/gestion/usuarios/buscar/`, `/gestion/usuarios/crear/`
  - `/gestion/usuarios/editar/<id>/`, `/gestion/usuarios/eliminar/<id>/`
- Materiales (CRUD y búsqueda):
  - Libros: `/libros/`, `/alta-libro/`, `/baja-libro/`, `/editar-libro/<id>/`, `/buscar-libros/?q=`
  - Mapas: `/mapas/`, `/alta-mapa/`, `/baja-mapa/`, `/editar-mapa/<id>/`, `/buscar-mapas/?q=`
  - Multimedia: `/multimedia/`, `/alta-multimedia/`, `/baja-multimedia/`, `/editar-multimedia/<id>/`, `/buscar-multimedia/?q=`
  - Notebooks: `/notebook/`, `/alta-notebook/`, `/baja-notebook/`, `/editar-notebook/<id>/`, `/buscar-notebooks/?q=`
  - Proyectores: `/proyector/`, `/alta-proyector/`, `/baja-proyector/`, `/editar-proyector/<id>/`, `/buscar-proyectores/?q=`
  - Varios: `/varios/`, `/alta-varios/`, `/baja-varios/`, `/editar-varios/<id>/`, `/buscar-varios/?q=`
  - Programas: `/programas/`, `/alta-programa/`, `/baja-programa/`, `/editar-programa/<id>/`
- Préstamos:
  - `/solicitar-prestamo/<libro_id>/`, `/gestionar-prestamos/`
  - `/aprobar-prestamo/<prestamo_id>/`, `/rechazar-prestamo/<prestamo_id>/`, `/finalizar-prestamo/<prestamo_id>/`
- CSV:
  - `/cargar-csv/` (subir archivo) y `/success/` (confirmación)

> Nota: existen rutas "mejoradas" (edición/baja/reactivación/registro) con sufijo `-mejorado` para cada tipo de material.

## 🗂️ Estructura del proyecto

- `biblioteca_digital/`: configuración del proyecto (settings, urls, wsgi/asgi).
- `materiales/`: app principal (models, views, urls, templates, static, management/commands).
  - `management/commands/delete_material.py`: comando para eliminar registros por tipo y `pk`.
  - `templates/`: vistas HTML, formularios y pantallas de gestión.
  - `static/`: CSS/JS/imagenes.

## 🧪 Comandos útiles

- Eliminar material por tipo y `pk` (management command):
  `python manage.py delete_material --tipo libro --id 123`
- Ejecutar tests:
  `python manage.py test materiales`

## 🔐 Usuarios y roles

- `AUTH_USER_MODEL = materiales.Usuario`.
- El acceso a la gestión está limitado a `perfil = bibliotecaria`.
- Protección para no eliminar el último usuario con perfil `bibliotecaria`.

## ✅ Buenas prácticas

- Usa las vistas para preparar datos; reserva la lógica de presentación al template.
- Evita consultas pesadas dentro de templates; utiliza endpoints de búsqueda (`/buscar-*`).
- Para producción: ajusta `DEBUG=False`, configura `ALLOWED_HOSTS`, `STATIC_ROOT` y base de datos.

---

Si encuentras inconsistencias o quieres mejorar el flujo (por ejemplo, paginación en listados, validaciones extra, o un `.env` formal), abre un issue o envía un PR. ¡Gracias por contribuir! 💻✨

