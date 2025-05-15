# Guía de Configuración del Proyecto Biblioteca

## 1. Requisitos Previos
- **Python:** Versión 3.8 o superior
- **pip:** Gestor de paquetes de Python
- **Git:** Control de versiones
- **Entorno virtual recomendado:** venv o conda

### Instalación de Requisitos
```bash
# Crear entorno virtual
python -m venv biblioteca_env

# Activar entorno virtual
# En Windows
biblioteca_env\Scripts\activate
# En Unix/MacOS
source biblioteca_env/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## 2. Configuración de Entornos

### Desarrollo
- **Archivo:** `.env.development`
- **Configuraciones:**
  - `DEBUG = True`
  - `DATABASE_URL = sqlite:///db.sqlite3`

### Producción
- **Archivo:** `.env.production`
- **Configuraciones:**
  - `DEBUG = False`
  - `ALLOWED_HOSTS = ['biblioteca.instituto210.edu.ar']`
  - `DATABASE_URL = postgresql://usuario:clave@host:puerto/basedatos`

## 3. Variables de Configuración

### Backend (Django)
- `SECRET_KEY`: Clave secreta para firma criptográfica
- `DEBUG`: Modo de depuración (True/False)
- `ALLOWED_HOSTS`: Hosts permitidos para la aplicación

### Configuraciones Principales
```python
# En settings.py
SECRET_KEY = 'django-insecure-...'  # Cambiar en producción
DEBUG = True  # Desactivar en producción
ALLOWED_HOSTS = []  # Configurar hosts válidos

# Directorios de archivos estáticos
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'views' / 'static',
    BASE_DIR / 'libros' / 'static',
]

# Configuración de medios
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Buenas Prácticas
- **Seguridad:** Nunca exponer la `SECRET_KEY`
- **Producción:** Desactivar `DEBUG`
- **Hosts:** Configurar `ALLOWED_HOSTS`

## 4. Comandos Básicos

### Backend (Django)
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor de desarrollo
python manage.py runserver
```

### Frontend
```bash
# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm start

# Construir para producción
npm run build
```

## 5. Comandos Git
```bash
# Clonar repositorio
git clone https://github.com/catriel458/biblioteca-210-insti.git

# Crear rama nueva
git checkout -b feature/nueva-funcionalidad

# Cambiar a rama principal
git checkout main

# Actualizar repositorio local
git pull origin main
```

## 6. Detener Servicios
```bash
# En Windows
taskkill /F /IM python.exe

# En Unix/MacOS
pkill python
```

**Nota:** Siempre usar entorno virtual y mantener actualizadas las dependencias.

