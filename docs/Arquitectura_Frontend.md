# Arquitectura del Frontend Biblioteca

## Componentes Clave

### 1. Vistas y Controladores
- **Vistas Django**: Gestionan la lógica de presentación y flujo de datos.
- **Formularios**: Manejan la entrada y validación de datos del usuario.
- **Plantillas HTML**: Definen la estructura y presentación de la interfaz.

### 2. Componentes Interactivos
- Formularios dinámicos para alta, modificación y eliminación de recursos.
- Tablas de listado con paginación y filtros.
- Modales y mensajes de confirmación.

## Flujo de Autenticación

### Sistema SIMEF
1. Ingreso de credenciales en página de login.
2. Verificación de usuario y contraseña.
3. Creación de sesión segura.
4. Acceso al apartado Biblioteca dentro de SIMEF.

### Flujo de Navegación
- Inicio de sesión
- Selección de módulo Biblioteca
- Acceso a diferentes secciones según permisos

## Estructura de Proyecto

```
├── biblioteca_digital/
│   ├── views/
│   │   ├── templates/          # Plantillas HTML
│   │   │   ├── materiales/
│   │   │   └── modals/
│   │   ├── static/            # Archivos estáticos
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── img/
│   │   └── forms.py           # Definición de formularios
```

## Tecnologías Clave

### Frontend
- **Django Template Engine**: Motor de plantillas para renderizado dinámico.
- **HTML5**: Estructura semántica de páginas.
- **CSS3**: Estilos y diseño responsivo.
- **JavaScript (Vanilla JS)**: Interactividad y validaciones del lado del cliente.

## 🖥️ Ejemplos de Código Frontend

### 📄 Página de Inicio (`home.html`)
```html
{% extends 'components/baseb.html' %}
{% load static %}

{% block content %}
<div class="container-fluid position-relative">
    <div class="row d-flex align-items-center">
        <div class="col-lg-6 logo-background">
            <img src="{% static 'imagenes/LogoBiblioteca.png' %}" alt="Logo Biblioteca">
        </div>
        
        <div class="col-lg-6 transparencia">
            <div class="content-overlay">
                <a class="btn btn-home" href="{% url 'prestamos' %}">PRESTAMOS</a>
                <a class="btn btn-home" href="{% url 'alta_material' %}">ALTA MATERIAL</a>
            </div>
        </div>
    </div>       
</div>
{% endblock %}
```

### 📋 Formulario de Alta de Material (`alta_material.html`)
```html
{% extends 'components/baseb.html' %}
{% load static %}

{% block content %}
<div class="container-fluid">
    <form id="form_alta_material" action="{% url 'alta_material' %}" method="POST">
        {% csrf_token %}
        <div class="row">
            <div class="col-12 col-lg-10">
                <div class="form-group">
                    <label for="tipo_material">Tipo de Material:</label>
                    <select class="form-control" id="tipo_material" name="tipo_material" required>
                        <option value="libro">Libro</option>
                        <option value="mapa">Mapa</option>
                        <option value="multimedia">Multimedia</option>
                        <option value="notebook">Notebook</option>
                        <option value="programa">Programa</option>
                        <option value="proyector">Proyector</option>
                        <option value="varios">Varios</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="cant_ejemplares">Cantidad de Ejemplares:</label>
                    <input type="number" class="form-control" id="cant_ejemplares" name="cant_ejemplares" min="1" value="1">
                </div>
            </div>
        </div>
    </form>
</div>
{% endblock %}
```

### 🎨 Estilos Dinámicos

### 🖼️ Patrón de Header Dinámico

A partir de la versión 2025-05:

- El header principal se define en el template base (`baseb.html`) y recibe una clase dinámica mediante el bloque `{% block header_class %}`.
- El contenido del header se define en `components/header.html` y utiliza clases como `header-home` o `header-pantalla` para aplicar fondos y estilos personalizados.

**Ejemplo de uso:**

```django
{% block header_class %}header-pantalla{% endblock %}
```

Esto permite personalizar el fondo y la altura del header según la vista.


```html
{% block extra_styles %}
<style>
    .logo-trans-background {
        background-image: url("{% static 'imagenes/LogoTrans.png' %}");
        background-size: cover;
    }
</style>
{% endblock %}
```

### 🔧 Características Técnicas
- **Template Engine:** Django Template Language
- **Frameworks CSS:** Bootstrap
- **Responsive Design:** Diseño adaptativo para múltiples dispositivos
- **Componentes Reutilizables:** Herencia de plantillas

### Librerías y Herramientas
- **Bootstrap**: Framework de diseño responsivo.
- **jQuery**: Manipulación del DOM y peticiones AJAX.

### Prácticas de Desarrollo
- Diseño responsivo
- Validación de formularios
- Manejo de estados de interfaz
- Optimización de carga y rendimiento

