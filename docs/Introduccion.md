# Introducción al Proyecto Biblioteca 210

## 🌐 Visión General

### Descripción del Proyecto
Biblioteca 210 es un sistema integral de gestión bibliotecaria diseñado específicamente para instituciones educativas. Desarrollado con el objetivo de modernizar y optimizar la administración de recursos educativos.

### Misión
- Transformar la gestión tradicional de bibliotecas
- Facilitar el acceso y control de recursos educativos
- Proporcionar herramientas tecnológicas para bibliotecarios y usuarios

## 🚀 Tecnologías Principales

### Backend
- **Lenguaje:** Python
- **Framework:** Django 5.x
- **Base de Datos:** SQLite (desarrollo), PostgreSQL (producción)
- **ORM:** Django Models
- **Autenticación:** Sistema SIMEF

### Frontend
- **Lenguaje:** HTML5, CSS3, JavaScript
- **Framework:** Django Template Engine
- **Diseño Responsivo:** Bootstrap

### Infraestructura
- **Control de Versiones:** Git
- **Repositorio:** GitHub
- **Despliegue:** Pendiente (posibles opciones: Heroku, DigitalOcean)

## 🛠 Primeros Pasos

### Requisitos
- Python 3.8+
- pip
- Entorno virtual (venv/conda)
- Git

### Instalación Rápida
```bash
# Clonar repositorio
git clone https://github.com/catriel458/biblioteca-210-insti.git

# Crear entorno virtual
python -m venv biblioteca_env

# Activar entorno
biblioteca_env\Scripts\activate  # Windows
source biblioteca_env/bin/activate  # Unix/MacOS

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
python manage.py migrate

# Ejecutar servidor
python manage.py runserver
```

## 📚 Documentación Relacionada

### Guías Principales
- [Arquitectura del Sistema](/docs/Arquitectura.md)
- [Configuración](/docs/Configuracion.md)
- [Convenciones de Código](/docs/Convenciones.md)
- [Tipos de Datos](/docs/Tipos.md)

### Recursos Adicionales
- Documentación de Django
- Guías de mejores prácticas de desarrollo
- Tutoriales de gestión bibliotecaria

## 🤝 Contribución
- Leer [CONTRIBUTING.md](CONTRIBUTING.md)
- Seguir guías de estilo
- Reportar issues en GitHub

## 📞 Contacto
- **Correo:** soporte.biblioteca@instituto210.edu.ar
- **Repositorio:** [GitHub Biblioteca 210](https://github.com/catriel458/biblioteca-210-insti)

**Última actualización:** Mayo 2025

