# Convenciones de Código Biblioteca

## 1. Nomenclatura General
- **Archivos y Carpetas:**
  - Nombres en minúsculas
  - Sin espacios
  - Usar guiones bajos para separar palabras
  - Ejemplos: `alta_material.py`, `gestion_usuarios/`

- **Clases y Modelos:**
  - Usar PascalCase
  - En español
  - Ejemplos: `Libro`, `Material`, `ControlPrestamos`

- **Funciones y Variables:**
  - Minúsculas con guiones bajos
  - Descriptivas y concisas
  - Ejemplos: `crear_prestamo()`, `total_libros`

## 2. Estructura de Archivos

### Backend (Django)
```
biblioteca_digital/
│
├── materiales/
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Lógica de vistas
│   ├── admin.py           # Configuración admin
│   ├── tests.py           # Pruebas unitarias
│   └── migrations/        # Migraciones de base de datos
│
├── usuarios/
│   ├── models.py
│   ├── views.py
│   └── forms.py
│
└── utils/                 # Funciones y clases de utilidad
```

### Frontend
```
views/
│
├── static/
│   ├── css/               # Hojas de estilo
│   ├── js/                # Scripts
│   └── img/               # Imágenes
│
└── templates/
    ├── base.html          # Plantilla base
    ├── materiales/        # Templates de materiales
    └── materiales/            # Templates de libros
```

## 3. Buenas Prácticas

### Convención de Headers en Plantillas

- El `<header>` debe ser único y definido en el template base.
- Utilizar el bloque `{% block header_class %}` para asignar clases que definan el fondo y estilos del header.
- El contenido interno del header debe estar en `components/header.html` y usar clases como `header-home` o `header-pantalla` según el contexto de la vista.


### Desarrollo
- Mantener funciones cortas y con un único propósito
- Usar type hints en Python
- Documentar con docstrings
- Validar datos en el lado del servidor
- Manejar excepciones de manera explícita

### Seguridad
- Nunca exponer credenciales en el código
- Usar variables de entorno para datos sensibles
- Implementar autenticación y autorización robusta
- Sanitizar inputs del usuario

### Rendimiento
- Optimizar consultas a base de datos
- Usar caché cuando sea apropiado
- Evitar consultas N+1
- Minimizar uso de recursos en bucles

## 4. Estructura de Commits

### Formato de Mensaje
```
<tipo>: <descripción corta>

[cuerpo opcional]

[pie opcional]
```

### Tipos de Commits
- `feat:` Nueva funcionalidad
- `fix:` Corrección de errores
- `docs:` Cambios en documentación
- `style:` Formato de código
- `refactor:` Restructuración de código
- `test:` Añadir o corregir tests
- `chore:` Tareas de mantenimiento

### Ejemplos
- `feat: Agregar sistema de préstamos de libros`
- `fix: Corregir validación de formulario de alta de material`
- `docs: Actualizar README con instrucciones de instalación`

## 5. Requisitos Pull Requests (PR)

### Criterios de Revisión
1. **Código**
   - Cumple con convenciones de estilo
   - Sin errores de linting
   - Pruebas unitarias pasando

2. **Documentación**
   - Descripción clara de cambios
   - Actualizar documentación si es necesario

3. **Revisión de Pares**
   - Al menos un revisor aprueba
   - Discusión constructiva

### Proceso de Merge
- Rebase o squash de commits
- Eliminar rama después de merge
- Actualizar rama main/master

### Checklist PR
- [ ] Código cumple estándares
- [ ] Pruebas añadidas/actualizadas
- [ ] Documentación actualizada
- [ ] Revisión de pares completada

